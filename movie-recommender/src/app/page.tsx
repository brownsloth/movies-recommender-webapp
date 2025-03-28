"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";

const questions = [
  {
    text: "What mood are you in right now?",
    options: ["Happy", "Sad", "Excited", "Relaxed"]
  },
  {
    text: "Do you prefer movies or TV shows?",
    options: ["Movies", "TV Shows"]
  },
  {
    text: "How much time do you have to watch something?",
    options: ["Less than 30 minutes", "1 hour", "2+ hours"]
  },
  {
    text: "Pick a genre you like:",
    options: ["Action", "Comedy", "Drama", "Sci-Fi", "Horror"]
  },
  {
    text: "Do you want something light or deep/intense?",
    options: ["Light", "Deep/Intense"]
  }
];

const recommendations = [
  ["Inception", "Black Mirror", "Interstellar"],
  ["Parks and Recreation", "Brooklyn Nine-Nine", "The Good Place"],
  ["The Godfather", "Breaking Bad", "The Wire"],
  ["Stranger Things", "The Matrix", "Blade Runner 2049"],
  ["Friends", "The Office", "Modern Family"]
];

// const genreSchema = [
//   "Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary",
//   "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical", "Mystery",
//   "Romance", "Sci-Fi", "Thriller", "War", "Western", "(no genres listed)"
// ];

function encodeAnswers(answers) {
  const vector = [];

  const answerMap = {
    0: questionEncoding.mood,
    1: questionEncoding.type,
    2: questionEncoding.time,
    3: questionEncoding.genre,
    4: questionEncoding.intensity
  };

  answers.forEach((entry, i) => {
    const options = answerMap[i];
    const oneHot = options.map((opt) => (opt === entry.answer ? 1 : 0));
    vector.push(...oneHot);
  });

  return vector;
}

export default function MovieRecommendationApp() {
  const [genreSchema, setGenreSchema] = useState<string[]>([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [startTime, setStartTime] = useState(Date.now());
  const [done, setDone] = useState(false);
  const [result, setResult] = useState([]);
  const [hasMounted, setHasMounted] = useState(false);
  useEffect(() => {
    setHasMounted(true);
  }, []);


  useEffect(() => {
    console.log("Fetching genre schema...");
    fetch("http://localhost:8000/genres")
      .then(res => {
        console.log("Received response:", res);
        return res.json();
      })
      .then(data => {
        console.log("Parsed genres:", data.genres);
        setGenreSchema(data.genres || []);
      })
      .catch(err => console.error("Failed to fetch genres:", err));
  }, []);


  const questionEncoding = {
    mood: ["Happy", "Sad", "Excited", "Relaxed"],
    type: ["Movies", "TV Shows"],
    time: ["Less than 30 minutes", "1 hour", "2+ hours"],
    genre: genreSchema, // ✅ now fetched from backend
    intensity: ["Light", "Deep/Intense"]
  };
  function encodeAnswers(answers) {
    const vector = [];

    const answerMap = {
      0: questionEncoding.mood,
      1: questionEncoding.type,
      2: questionEncoding.time,
      3: questionEncoding.genre,
      4: questionEncoding.intensity
    };

    answers.forEach((entry, i) => {
      const options = answerMap[i];
      const oneHot = options.map((opt) => (opt === entry.answer ? 1 : 0));
      vector.push(...oneHot);
    });

    return vector;
  }

  const handleAnswer = async (answer) => {
    const duration = Date.now() - startTime;
    const newAnswers = [...answers, { answer, duration }];
    setAnswers(newAnswers);

    if (current + 1 < questions.length) {
      setTimeout(() => {
        setCurrent(current + 1);
        setStartTime(Date.now());
      }, 300);
    } else {
      setDone(true);
      const userVector = encodeAnswers(newAnswers);
      try {
        const response = await fetch("http://localhost:8000/recommend", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ vector: userVector })
        });
        const data = await response.json();
        setResult(data.recommendations);
      } catch (err) {
        console.error("Recommendation fetch failed:", err);
      }
      // const index = newAnswers.reduce((sum, a, i) => sum + i * (a.duration % 5), 0) % recommendations.length;
      // setResult(recommendations[index]);
    }
  };
  if (!genreSchema || !hasMounted || genreSchema.length === 0) {
    return <div>Loading...</div>;
  }

  if (done) {
    return (
      <div className="p-6 min-h-screen flex flex-col items-center justify-center bg-black text-white">
        <h2 className="text-2xl font-bold italic mb-4">Your Recommendations:</h2>
        <ul className="list-disc list-inside text-lg">
          {result.map((movie, index) => (
            <li key={index}>
              {movie.title} — <span className="text-sm italic text-gray-400">score: {movie.score}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  }

  const currentQuestion = questions[current];

  return (
    <div
      className="relative min-h-screen w-screen bg-black text-white overflow-hidden flex items-center justify-center"
      style={{
        // backgroundImage: "url('/image.png')",
        backgroundRepeat: "no-repeat",
        backgroundSize: "100% 100%",
        backgroundPosition: "center center"
      }}
    >

      <AnimatePresence mode="wait">
        <motion.div
          key={current}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3 }}
        >
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-4">
            <h2 className="text-4xl italic font-semibold mb-6 max-w-3xl">
              {currentQuestion.text}
            </h2>
            <div className="flex flex-wrap justify-center gap-4">
              {currentQuestion.options.map((option, idx) => (
                <Button key={idx} onClick={() => handleAnswer(option)}>{option}</Button>
              ))}
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

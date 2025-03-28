import * as React from "react";

export function Card({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className="rounded-xl border p-4 shadow" {...props}>{children}</div>;
}

export function CardContent({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className="mt-2" {...props}>{children}</div>;
}

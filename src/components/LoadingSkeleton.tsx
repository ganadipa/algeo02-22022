import React from "react";

//
export default function SkeletonLoading({
  className,
  color,
}: {
  className?: string;
  color?: string;
}) {
  return (
    <div className={`${className} animate-pulse md:flex md:items-center`}>
      <div
        className={`flex h-full w-full items-center justify-center ${color} rounded dark:bg-gray-700`}
        content=""
      ></div>
    </div>
  );
}

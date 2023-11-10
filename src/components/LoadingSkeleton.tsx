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
    <div
      role="status"
      className={`${className} animate-pulse space-y-8 md:flex md:items-center md:space-x-8 md:space-y-0`}
    >
      <div
        className={`flex h-full w-full items-center justify-center ${color} rounded dark:bg-gray-700 sm:w-96`}
        content=""
      ></div>
    </div>
  );
}

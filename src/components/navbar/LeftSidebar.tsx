"use client";

import { sidebarLinks } from "../../../constant";
import React from "react";

import { usePathname } from "next/navigation";
import Image from "next/image";
import Link from "next/link";

const LeftSidebar = () => {
  const pathname = usePathname();

  return (
    <section className="background-light900_dark200 light-border flex-center sticky left-0 top-0 mb-3 flex w-full flex-col overflow-y-auto border-b  border-green-200 p-6 shadow-light-300 dark:shadow-none">
      <div className="flex flex-col gap-8">
        <div className="flex flex-1 flex-row gap-4">
          {sidebarLinks.map((item) => {
            const isActive =
              (pathname.includes(item.route) && item.route.length > 1) ||
              pathname === item.route;
            return (
              <Link
                key={item.route}
                href={item.route}
                className={`${
                  isActive
                    ? "primary-gradient rounded-lg text-light-900"
                    : "text-dark300_light900"
                } flex items-center justify-start gap-4 bg-transparent p-4`}
              >
                <Image
                  src={item.imgURL}
                  alt={item.label}
                  width={20}
                  height={20}
                  className={`${isActive ? "" : ""}`}
                />
                <p
                  className={`${
                    isActive ? "base-bold" : "base-medium"
                  } max-lg:hidden`}
                >
                  {item.label}
                </p>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default LeftSidebar;

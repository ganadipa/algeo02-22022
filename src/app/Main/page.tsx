"use client";

import FileUpload from "@/component/FileUpload";
import SkeletonLoading from "@/component/LoadingSkeleton";
import Image from "next/image";
import React, { useEffect, useState } from "react";

import * as z from "zod";

const formSchema = z.object({
  username: z.string().min(2).max(50),
});

const Main = () => {
  const [loading, setLoading] = useState<boolean>(true);

  // temporary
  const [secs, setSecs] = useState(0);
  const [filename, setFilename] = useState("hello");

  useEffect(() => {
    setTimeout(() => {
      setLoading((loading) => !loading);
      setSecs((secs) => secs + 1);
    }, 3000);
  }, [secs]);

  return (
    <div className="max-md:bg-white">
      {/* reverse image search */}
      <section className="">
        <h1>Reverse Image Search</h1>
        <main className="flex flex-col w-full">
          <div className="h-24 aspect-video relative">
            {loading ? (
              <SkeletonLoading className="w-full h-full" />
            ) : (
              <Image
                src="/sunflower.jpg"
                alt=""
                fill
                objectFit="cover"
                className="rounded"
              />
            )}
          </div>
          <div>
            <FileUpload />
          </div>
        </main>
      </section>
      <hr className="border-[1.5px] rounded-full  border-slate-500" />
      {/* search result */}
      <section className="text-red-500">
        <h1>Reverse Image Search</h1>
        Hello World!
      </section>
    </div>
  );
};

export default Main;

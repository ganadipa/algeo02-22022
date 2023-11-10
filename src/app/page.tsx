// @ts-nocheck
/* eslint-disable */

"use client";

import FileUpload from "../components/FileUpload";
import SkeletonLoading from "../components/LoadingSkeleton";
import IMAGE_RESULT from "../../constant/Main";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

type PagingButtonHelperProps = {
  numpage: number;
  maxpage: number;
  setNumpage: React.Dispatch<React.SetStateAction<number>>;
};

type MainPageProps = {
  searchParams: { [key: string]: string | string[] | undefined };
};

const ShowGreaterThan3 = ({ numpage, maxpage }: PagingButtonHelperProps) => {
  const showLeftDotDot = numpage > 3;
  const showRightDotDot = maxpage - numpage > 2;

  const intersectWithFirst = numpage < 3;
  const intersectWithLast = numpage > maxpage - 2;

  return (
    <>
      {numpage === 1 || (
        <div
          className={`border- flex items-center justify-center border${
            numpage == 1 ? "blue-300" : "red-400"
          } h-6 w-6`}
        >
          <button className="" onClick={() => setNumpage(1)}>
            {1}
          </button>
        </div>
      )}
      {showLeftDotDot && <p>...</p>}
      {intersectWithFirst || (
        <div
          className={`border- flex items-center justify-center border-red-400 h-6 w-6`}
        >
          <button className="" onClick={() => setNumpage(numpage - 1)}>
            {numpage - 1}
          </button>
        </div>
      )}
      <div
        className={`border- flex items-center justify-center border-blue-300 h-6 w-6`}
      >
        <button className="" onClick={() => setNumpage(numpage)}>
          {numpage}
        </button>
      </div>
      {intersectWithLast || (
        <div
          className={`border- flex items-center justify-center border-red-400 h-6 w-6`}
        >
          <button className="" onClick={() => setNumpage(numpage + 1)}>
            {numpage + 1}
          </button>
        </div>
      )}
      {showRightDotDot && <p>...</p>}
      {numpage == maxpage || (
        <div
          key={maxpage}
          className={`border- flex items-center justify-center border${
            numpage == maxpage ? "blue-300" : "red-400"
          } h-6 w-6`}
        >
          <button className="" onClick={() => setNumpage(maxpage)}>
            {maxpage}
          </button>
        </div>
      )}
    </>
  );
};

const ShowLessThan4 = ({
  numpage,
  maxpage,
  setNumpage,
}: PagingButtonHelperProps) => {
  const numList = Array.from({ length: maxpage }, (_, index) => index + 1);
  return (
    <>
      {numList.map((num) => {
        return (
          <div
            key={num}
            className={`border- flex items-center justify-center border${
              numpage == num ? "blue-300" : "red-400"
            } h-6 w-6`}
          >
            <button className="" onClick={() => setNumpage(num)}>
              {num}
            </button>
          </div>
        );
      })}
    </>
  );
};

const Main = ({ searchParams }: MainPageProps) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [numpage, setNumpage] = useState<number>(1);
  const [datasetUploaded, setDatasetUploaded] = useState(true);
  const router = useRouter();

  const idxMin = (numpage - 1) * 6;
  const idxMax = Math.min(IMAGE_RESULT.length, numpage * 6);
  const SHOWING_IMAGES = IMAGE_RESULT.slice(idxMin, idxMax);
  const maxpage = Math.ceil(IMAGE_RESULT.length / 6);

  // temporary
  const [secs, setSecs] = useState(0);
  const [filename, setFilename] = useState("hello");
  const [loadingImages, setLoadingImages] = useState([
    true,
    true,
    true,
    true,
    true,
    true,
  ]);

  useEffect(() => {
    setTimeout(() => {
      setLoading((loading) => !loading);
      setSecs((secs) => secs + 1);
    }, 3000);
  }, [secs]);

  return (
    <div className="flex flex-col items-center justify-center">
      {/* Title */}
      <h1>Reverse Image Search</h1>

      <main className="flex h-full flex-col">
        <section className="flex w-full flex-col items-center justify-center">
          <div className="relative aspect-video max-md:w-[300px] md:w-[450px]">
            {loading ? (
              <SkeletonLoading
                className="h-full w-full animate-pulse"
                color="bg-gray-300"
              />
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
        </section>
        {/* result section */}

        <hr className="rounded-full border-[1.5px]  border-slate-500" />
        {/* search result */}
        <section className="flex w-full flex-col ">
          <div className="flex flex-row justify-between">
            <h4>Result</h4>
            <p>{IMAGE_RESULT.length} Results in 0.57 seconds.</p>
          </div>

          <div className="grid grid-cols-2 gap-4 max-md:h-[50vh] md:grid-cols-3">
            {SHOWING_IMAGES.map((img, ind) => {
              return (
                <div key={ind} className="relative">
                  <Image src={img.url} alt="" width={500} height={500} />
                  <span className="absolute left-1/2 top-0 text-white">
                    {Math.round(img.similiarityrate)} %
                  </span>
                </div>
              );
            })}
          </div>

          {/* Pagination button */}
          <div className="flex flex-row justify-center gap-2">
            {/* Left arrow button */}
            {numpage != 1 && (
              <button onClick={() => setNumpage((numpage) => numpage - 1)}>
                &lt;
              </button>
            )}

            {/* Handle styling */}
            {maxpage > 3 ? (
              <ShowGreaterThan3 numpage={numpage} maxpage={maxpage} />
            ) : (
              <ShowLessThan4 numpage={numpage} maxpage={maxpage} />
            )}

            {/* Right arrow button */}
            {numpage != maxpage && (
              <button onClick={() => setNumpage((np) => np + 1)}>&gt;</button>
            )}
          </div>
        </section>

        <hr className="rounded-full border-[1.5px]  border-slate-500" />
        <div className="align-center flex flex-row justify-between">
          <button className="flex items-center justify-center">
            Upload Dataset
          </button>
          {datasetUploaded && <p>Dataset uploaded!</p>}
        </div>
      </main>
    </div>
  );
};

export default Main;

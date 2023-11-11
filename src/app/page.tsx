// @ts-nocheck
/* eslint-disable */

"use client";

import FileUpload, { searchResultType } from "../components/FileUpload";
import SkeletonLoading from "../components/LoadingSkeleton";
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

const ShowGreaterThan3 = ({
  numpage,
  maxpage,
  setNumpage,
}: PagingButtonHelperProps) => {
  const showLeftDotDot = numpage > 3;
  const showRightDotDot = maxpage - numpage > 2;

  const intersectWithFirst = numpage < 3;
  const intersectWithLast = numpage > maxpage - 2;

  return (
    <>
      {numpage === 1 || (
        <div
          className={`cursor-pointer border flex bg-white items-center justify-center h-6 w-6`}
          onClick={() => setNumpage(1)}
        >
          <button className="" onClick={() => setNumpage(1)}>
            {1}
          </button>
        </div>
      )}
      {showLeftDotDot && <p>...</p>}
      {intersectWithFirst || (
        <div
          className={`border flex items-center justify-center bg-white h-6 w-6`}
          onClick={() => setNumpage(numpage - 1)}
        >
          <button className="">{numpage - 1}</button>
        </div>
      )}
      <div
        className={`border flex items-center justify-center h-6 w-6 primary-gradient text-white font-semibold`}
        onClick={() => setNumpage(numpage)}
      >
        <button className="">{numpage}</button>
      </div>
      {intersectWithLast || (
        <div
          className={`border flex items-center justify-center bg-white h-6 w-6`}
          onClick={() => setNumpage(numpage + 1)}
        >
          <button className="">{numpage + 1}</button>
        </div>
      )}
      {showRightDotDot && <p>...</p>}
      {numpage == maxpage || (
        <div
          key={maxpage}
          className={`border flex items-center justify-center bg-white h-6 w-6`}
          onClick={() => setNumpage(maxpage)}
        >
          <button className="">{maxpage}</button>
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
            className={`border flex items-center justify-center border${
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
  const [selectedImage, setSelectedImage] = useState(false);
  const [searchResult, setSearchResult] = useState<searchResultType>({data: [], length: 0});
  const router = useRouter();

  const idxMin = (numpage - 1) * 6;
  const idxMax = Math.min(searchResult.data.length, numpage * 6);
  const SHOWING_IMAGES = searchResult.data.slice(idxMin, idxMax);
  const maxpage = Math.ceil(searchResult.data.length / 6);

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

  return (
    <div className="flex flex-col items-center justify-center">
      {/* Title */}
      <div className="bg-white px-12 py-4 mb-2 rounded">
        <h1 class="bg-gradient-to-r from-[#28d87b] to-[#57af95] inline-block text-transparent bg-clip-text font-bold md:text-3xl text-xl">
          Reverse Image Search
        </h1>
      </div>

      <main className="flex h-full flex-col">
        <section className="flex w-full max-md:flex-col md:flex-row gap-16 items-center justify-center mb-4">
          <div className="relative max-md:aspect-video max-md:w-[300px] md:w-[450px] aspect-video">
            {loading ? (
              <SkeletonLoading
                className="h-full w-full animate-pulse"
                color="bg-gray-300"
              />
            ) : (
              <Image
                src={selectedImage}
                alt=""
                fill
                objectFit="cover"
                className="rounded"
              />
            )}
          </div>
          <div>
            <FileUpload
              setLoading={setLoading}
              setSelectedImage={setSelectedImage}
              setSearchResult = {setSearchResult}
            />
          </div>
        </section>
        {/* result section */}

        <hr className="rounded-full border-[1.5px] border-slate-500" />
        {/* search result */}
        <section className="flex w-full flex-col ">
          <div className="flex flex-row justify-between mb-4">
            <h4 className="text-green-400 font-semibold">Result</h4>
            <p>{searchResult.data.length} Results in {Math.floor(searchResult.duration)} seconds.</p>
          </div>

          <div className="grid grid-cols-2 gap-4 max-md:h-[50vh] md:grid-cols-3 mb-4">
            {SHOWING_IMAGES.map((img, ind) => {
              return (
                <div key={ind} className="relative aspect-video md:w-[33vh]">
                  <Image src={img.image} alt="" fill objectFit="cover" />
                  <div className="primary-gradient rounded absolute left-0 top-0 text-white px-2 py-0.5">
                    <span className="">
                      {img.similiarityRate.toFixed(2)*100} %
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Pagination button */}
          <div className="flex flex-row justify-center gap-2 mb-4">
            {/* Left arrow button */}
            {numpage != 1 && (
              <button onClick={() => setNumpage((numpage) => numpage - 1)}>
                &lt;
              </button>
            )}

            {/* Handle styling */}
            {maxpage > 3 ? (
              <ShowGreaterThan3
                numpage={numpage}
                maxpage={maxpage}
                setNumpage={setNumpage}
              />
            ) : (
              <ShowLessThan4
                numpage={numpage}
                maxpage={maxpage}
                setNumpage={setNumpage}
              />
            )}

            {/* Right arrow button */}
            {numpage != maxpage && (
              <button onClick={() => setNumpage((np) => np + 1)}>&gt;</button>
            )}
          </div>
        </section>

        <hr className="rounded-full border-[1.5px]  border-slate-500" />
      </main>
    </div>
  );
};

export default Main;

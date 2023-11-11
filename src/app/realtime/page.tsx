"use client";

import SkeletonLoading from "../../components/LoadingSkeleton";
import IMAGE_RESULT from "../../../constant/Main";
import Image from "next/image";
import React, { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import RTFileUpload from "@/src/components/RTFileUpload";

type PagingButtonHelperProps = {
  numpage: number;
  maxpage: number;
  setNumpage: React.Dispatch<React.SetStateAction<number>>;
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
          className={`flex h-6 w-6 cursor-pointer items-center justify-center border bg-white`}
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
          className={`flex h-6 w-6 items-center justify-center border bg-white`}
          onClick={() => setNumpage(numpage - 1)}
        >
          <button className="">{numpage - 1}</button>
        </div>
      )}
      <div
        className={`primary-gradient flex h-6 w-6 items-center justify-center border font-semibold text-white`}
        onClick={() => setNumpage(numpage)}
      >
        <button className="">{numpage}</button>
      </div>
      {intersectWithLast || (
        <div
          className={`flex h-6 w-6 items-center justify-center border bg-white`}
          onClick={() => setNumpage(numpage + 1)}
        >
          <button className="">{numpage + 1}</button>
        </div>
      )}
      {showRightDotDot && <p>...</p>}
      {numpage === maxpage || (
        <div
          key={maxpage}
          className={`flex h-6 w-6 items-center justify-center border bg-white`}
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
            className={` flex items-center justify-center${
              numpage === num ? " border-blue-300" : " border-red-400"
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

function RealTime() {
  const [captured, setCaptured] = useState<string | null>("");
  const webcamRef = useRef<Webcam | null>(null);

  function captureImage() {
    if (!webcamRef.current) return;
    const ss = webcamRef.current.getScreenshot();
    console.log(ss);
    setCaptured(ss);
  }

  useEffect(() => {
    setTimeout(captureImage, 5000);
  }, [captured]);

  return (
    <div className="flex flex-col gap-4">
      {/* Title */}
      <div className="mb-4 self-center rounded-xl bg-white px-12 py-4">
        <h1 className="inline-block bg-gradient-to-r from-[#28d87b] to-[#57af95] bg-clip-text text-xl font-bold text-transparent md:text-3xl">
          Real Time Reverse Image Search
        </h1>
      </div>
      <div className="flex flex-col items-center justify-around md:flex-row">
        <Webcam ref={webcamRef} />
        <Main captured={captured} />
      </div>
    </div>
  );
}

const Main = ({ captured }: { captured: string | null }) => {
  const [numpage, setNumpage] = useState<number>(1);
  const [selectedImage, setSelectedImage] = useState<
    string | ArrayBuffer | null
  >(null);

  const idxMin = (numpage - 1) * 6;
  const idxMax = Math.min(IMAGE_RESULT.length, numpage * 6);
  const SHOWING_IMAGES = IMAGE_RESULT.slice(idxMin, idxMax);
  const maxpage = Math.ceil(IMAGE_RESULT.length / 6);

  return (
    <div className="flex flex-col items-center justify-center">
      <main className="flex h-full flex-col">
        <section className="mb-4 flex w-full items-center justify-center gap-16 max-md:flex-col md:flex-row">
          <div className="relative aspect-video max-md:aspect-video max-md:w-[300px] md:w-[450px]">
            {!captured ? (
              <SkeletonLoading
                className="h-full w-full animate-pulse"
                color="bg-gray-300"
              />
            ) : (
              <Image
                src={captured}
                alt=""
                fill
                objectFit="cover"
                className="rounded"
              />
            )}
          </div>
          <div>
            <RTFileUpload
              setSelectedImage={setSelectedImage}
              selectedImage={selectedImage}
            />
          </div>
        </section>
        {/* result section */}

        <hr className="rounded-full border-[1.5px] border-slate-500" />
        {/* search result */}
        <section className="flex w-full flex-col ">
          <div className="mb-4 flex flex-row justify-between">
            <h4 className="font-semibold text-green-400">Result</h4>
            <p>{IMAGE_RESULT.length} Results in 0.57 seconds.</p>
          </div>

          <div className="mb-4 grid grid-cols-2 gap-4 max-md:h-[50vh] md:grid-cols-3">
            {SHOWING_IMAGES.map((img, ind) => {
              return (
                <div key={ind} className="relative aspect-video md:w-[33vh]">
                  <Image src={img.url} alt="" fill objectFit="cover" />
                  <div className="primary-gradient absolute left-0 top-0 rounded px-2 py-0.5 text-white">
                    <span className="">
                      {Math.round(img.similiarityrate)} %
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Pagination button */}
          <div className="mb-4 flex flex-row justify-center gap-2">
            {/* Left arrow button */}
            {numpage !== 1 && (
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
            {numpage !== maxpage && (
              <button onClick={() => setNumpage((np) => np + 1)}>&gt;</button>
            )}
          </div>
        </section>

        <hr className="rounded-full border-[1.5px]  border-slate-500" />
      </main>
    </div>
  );
};

export default RealTime;

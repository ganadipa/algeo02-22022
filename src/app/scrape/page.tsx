"use client";

import FileUpload, {
  searchResultType,
} from "../../components/ScrapeFileUpload";
import SkeletonLoading from "../../components/LoadingSkeleton";
import Image from "next/image";
import React, { useState } from "react";

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
            className={`flex items-center justify-center ${
              numpage === num ? "border-blue-300" : "border-red-400"
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
  const [selectedImage, setSelectedImage] = useState<
    string | ArrayBuffer | null
  >(null);
  const [searchResult, setSearchResult] = useState<searchResultType>({
    data: [],
    duration: 0,
    ok: false,
    loading: false,
    upload_time: 0,
  });

  const idxMin = (numpage - 1) * 6;
  const idxMax = Math.min(searchResult.data.length, numpage * 6);
  const SHOWING_IMAGES = searchResult.data.slice(idxMin, idxMax);
  const maxpage = Math.ceil(searchResult.data.length / 6);

  return (
    <div className="flex flex-col items-center justify-center">
      {/* Title */}
      <div className="mb-2 rounded bg-white px-12 py-4">
        <h1 className="inline-block bg-gradient-to-r from-[#28d87b] to-[#57af95] bg-clip-text text-xl font-bold text-transparent md:text-3xl">
          Reverse Image Search
        </h1>
      </div>

      <main className="flex h-full flex-col">
        <section className="mb-4 flex w-full items-center justify-center gap-16 max-md:flex-col md:flex-row">
          <div className="relative aspect-video max-md:aspect-video max-md:w-[300px] md:w-[450px]">
            {loading ? (
              <SkeletonLoading
                className="h-full w-full animate-pulse"
                color="bg-gray-300"
              />
            ) : (
              <Image
                src={
                  selectedImage
                    ? typeof selectedImage === "string"
                      ? selectedImage
                      : Buffer.from(selectedImage).toString()
                    : "/sunflower.jpeg"
                }
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
              setSearchResult={setSearchResult}
              searchResult={searchResult}
              setNumpage={setNumpage}
            />
          </div>
        </section>
        {/* result section */}

        <hr className="rounded-full border-[1.5px] border-slate-500" />

        {/* search result */}
        {searchResult.ok ? (
          <section className="flex w-full flex-col ">
            <div className="mb-4 flex flex-row justify-between">
              <h4 className="font-semibold text-green-400">Result</h4>
              <p>
                {searchResult.data.length} Results in{" "}
                {searchResult.duration.toFixed(2)} seconds. With scraping time:{" "}
                {searchResult.upload_time.toFixed(2)} seconds.
                <br></br>
                Note that for scraping we show all the images scraped (not only
                the &gt;60% similiarity)
              </p>
            </div>

            <div className="mb-4 grid grid-cols-2 gap-4 max-md:h-[50vh] md:grid-cols-3">
              {SHOWING_IMAGES.map((img, ind) => {
                return (
                  <div
                    key={ind + numpage * 6}
                    className="relative aspect-video md:w-[33vh]"
                  >
                    <>
                      <Image src={img.image} alt="" fill objectFit="cover" />
                      <div className="primary-gradient absolute left-0 top-0 rounded px-2 py-0.5 text-white">
                        <span className="">
                          {Math.floor(img.similiarityRate * 100)} %
                        </span>
                      </div>
                    </>
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
        ) : searchResult.loading ? (
          <section className="flex w-full flex-col ">
            <div className="mb-4 flex flex-row justify-center">
              <p className="font-semibold text-white">Searching...</p>
            </div>

            <div className="mb-4 grid grid-cols-2 gap-4 max-md:h-[50vh] md:grid-cols-3">
              {Array.from({ length: 6 }).map((img, ind) => {
                return (
                  <div key={ind} className="relative aspect-video md:w-[33vh]">
                    <SkeletonLoading
                      className="h-full w-full animate-pulse"
                      color="bg-gray-300"
                    />
                  </div>
                );
              })}
            </div>
            <div
              className="mb-4 flex flex-row justify-center gap-2"
              content=""
            ></div>
          </section>
        ) : (
          <div className=" flex items-center justify-center">
            <p className="font-semibold">
              Please Upload the image and the dataset first, then click search
              by tekcture or color
            </p>
          </div>
        )}

        <hr className="rounded-full border-[1.5px]  border-slate-500" />
      </main>
    </div>
  );
};

export default Main;

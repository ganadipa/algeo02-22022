"use client";
import React, { useRef, useState } from "react";
import toast from "react-hot-toast";

const CBIREndpoint = "http://localhost:8000/api/upload-image/";

type responseType = {
  similiarityRate: number;
  image: string;
};
export type searchResultType = {
  data: responseType[];
  duration: number;
  ok: boolean;
  loading: boolean;
  upload_time: number;
};

type BackendResponseType = {
  duration: number;
  similiarity_arr: number[];
  dataset: string[];
  upload_time: number;
};

type FileUploadType = {
  setSelectedImage: React.Dispatch<
    React.SetStateAction<string | ArrayBuffer | null>
  >;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
  setSearchResult: React.Dispatch<searchResultType>;
  searchResult: searchResultType;
  setNumpage: React.Dispatch<React.SetStateAction<number>>;
};

const FileUpload = ({
  setSelectedImage,
  setLoading,
  setSearchResult,
  searchResult,
  setNumpage,
}: FileUploadType) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const handleChange: React.ChangeEventHandler<HTMLInputElement> | undefined = (
    e
  ) => {
    if (!e.target.files) return;
    const img = e.target.files[0];
    const reader = new FileReader();

    reader.addEventListener("load", () => {
      setSelectedImage(reader.result);
      setLoading(false);
    });

    reader.readAsDataURL(img);
  };

  async function handleSubmit(isColor: boolean) {
    try {
      setNumpage(1);
      const toastLoadingId = toast.loading("Searching...");
      const query = fileInputRef.current?.files;
      const formData = new FormData();

      if (!query || !searchQuery) {
        toast.error("Something went wrong!");
        toast.dismiss(toastLoadingId);
        return;
      }
      setSearchResult({
        data: [],
        duration: 0,
        ok: false,
        loading: true,
        upload_time: 0,
      });

      formData.append("scrape", searchQuery);
      formData.append("query", query[0] as File);
      formData.append("search_method", isColor ? "color" : "texture");

      const response = await fetch(CBIREndpoint, {
        method: "POST",
        mode: "cors",
        body: formData,
      });

      if (!response.ok) {
        setSearchResult({
          data: [],
          duration: 0,
          ok: false,
          loading: false,
          upload_time: 0,
        });
        toast.error("Something went wrong!");
        toast.dismiss(toastLoadingId);
        return;
      }

      const data: BackendResponseType = await response.json();

      const searchResultFromData: searchResultType = {
        data: [],
        duration: 0,
        ok: true,
        loading: false,
        upload_time: 0,
      };

      searchResultFromData.duration = data.duration;
      searchResultFromData.upload_time = data.upload_time;
      for (let i = 0; i < data.similiarity_arr.length; i++) {
        searchResultFromData.data.push({
          similiarityRate: data.similiarity_arr[i],
          image: data.dataset[i],
        });
      }

      setSearchResult(searchResultFromData);
      toast.success("Data result successfully arrived!");
      toast.dismiss(toastLoadingId);
    } catch (error) {
      console.error("Error during fetch:", error);
    }
  }

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h2 className="font-semibold text-[#28d87b]">Image upload</h2>
        <input
          type="file"
          name=""
          id="imageInput"
          accept="image/*"
          ref={fileInputRef}
          onChange={handleChange}
          className="cursor-pointer rounded-md bg-[#57af95] px-4 py-2 text-white hover:bg-green-600"
        />
      </div>
      <div className="flex flex-col items-center justify-between">
        <p>Use Scrape:</p>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>
      <div className="flex-between flex flex-row">
        {searchResult.loading ? (
          <></>
        ) : (
          <>
            <p>Search by: </p>
            <div className="flex flex-row max-md:gap-4 md:gap-8">
              <button
                className="rounded bg-slate-600 py-2 text-white max-md:px-2 md:w-[100px]"
                onClick={() => handleSubmit(false)}
              >
                Texture
              </button>
              <button
                className="rounded bg-slate-600 py-2 text-white max-md:px-2 md:w-[100px]"
                onClick={() => handleSubmit(true)}
              >
                Color
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default FileUpload;

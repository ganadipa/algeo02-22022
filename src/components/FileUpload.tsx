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
};

type BackendResponseType = {
  duration: number;
  similiarity_arr: number[];
  dataset: string[];
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
  const datasetInputRef = useRef<HTMLInputElement | null>(null);
  const [datasetUploaded, setDatasetUploaded] = useState<boolean>(false);

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
      const dataset = datasetInputRef.current?.files;
      const query = fileInputRef.current?.files;
      const formData = new FormData();

      if (!query || !dataset) {
        toast.error("Something went wrong!");
        toast.dismiss(toastLoadingId);
        return;
      }
      setSearchResult({
        data: [],
        duration: 0,
        ok: false,
        loading: true,
      });

      const datasetArray = Array.from(dataset);
      formData.append("query", query[0] as File);
      datasetArray.forEach((file, index) => {
        formData.append(`dataset[${index}]`, file);
      });
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
        });
        toast.error("Something went wrong!");
        toast.dismiss(toastLoadingId);
        return;
      }

      const data: BackendResponseType = await response.json();
      console.log(data);

      const searchResultFromData: searchResultType = {
        data: [],
        duration: 0,
        ok: true,
        loading: false,
      };

      searchResultFromData.duration = data.duration;
      for (let i = 0; i < data.similiarity_arr.length; i++) {
        searchResultFromData.data.push({
          similiarityRate: data.similiarity_arr[i],
          image: data.dataset[i],
        });
      }

      setDatasetUploaded(true);
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
        <h2 className="self-start font-semibold text-[#28d87b]">
          Dataset upload
        </h2>
        <input
          type="file"
          // @ts-ignore
          webkitdirectory=""
          multiple
          directory=""
          ref={datasetInputRef}
          onChange={() => setDatasetUploaded(true)}
          className="cursor-pointer rounded-md bg-[#57af95] px-4 py-2 text-white hover:bg-green-600"
        />
        {datasetUploaded && <p className="self-end">Dataset uploaded!</p>}
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

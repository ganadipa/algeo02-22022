"use client";
import React, { useRef, useState } from "react";

const CBIREndpoint = "http://localhost:8000/api/upload-image/";

type responseType = {
  similiarityRate: number;
  image: string;
};
export type searchResultType = {
  data: responseType[];
  duration: number;
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
};

const FileUpload = ({
  setSelectedImage,
  setLoading,
  setSearchResult,
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

  async function handleSubmit() {
    try {
      setLoading(true); // Assuming you want to set loading to true when submitting
      const dataset = datasetInputRef.current?.files;
      const query = fileInputRef.current?.files;
      const formData = new FormData();

      if (!query || !dataset) return; // nanti ganti pake toast kalo sempet

      const datasetArray = Array.from(dataset);
      formData.append("query", query[0] as File);
      datasetArray.forEach((file, index) => {
        formData.append(`dataset[${index}]`, file);
      });

      const response = await fetch(CBIREndpoint, {
        method: "POST",
        mode: "cors",
        body: formData,
      });

      if (!response.ok) {
        // Handle non-successful responses (e.g., server error)
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: BackendResponseType = await response.json();
      console.log(data);

      const searchResultFromData: searchResultType = {
        data: [],
        duration: 0,
      };

      searchResultFromData.duration = data.duration;
      for (let i = 0; i < data.similiarity_arr.length; i++) {
        searchResultFromData.data.push({
          similiarityRate: data.similiarity_arr[i],
          image: data.dataset[i],
        });
      }

      // Set datasetUploaded state based on the response
      setDatasetUploaded(true);
      setSearchResult(searchResultFromData);
    } catch (error) {
      console.error("Error during fetch:", error);
    } finally {
      setLoading(false); // Assuming you want to set loading to false when the request completes
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
        <p>Search by: </p>
        <div className="flex flex-row max-md:gap-4 md:gap-8">
          <button
            className="rounded bg-slate-600 py-2 text-white max-md:px-2 md:w-[100px]"
            onClick={handleSubmit}
          >
            Texture
          </button>
          <button
            className="rounded bg-slate-600 py-2 text-white max-md:px-2 md:w-[100px]"
            onClick={handleSubmit}
          >
            Color
          </button>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;

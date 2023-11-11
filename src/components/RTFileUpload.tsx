"use client";
import React, { useRef, useState } from "react";
import ToggleGroupDemo, { Toggle } from "@/src/components/ui/toggle";

const CBIREndpoint = "http://localhost:8000/api/upload-image/";

type RTFileUploadType = {
  setSelectedImage: React.Dispatch<
    React.SetStateAction<string | ArrayBuffer | null>
  >;
  selectedImage: string | ArrayBuffer | null;
};

const RTFileUpload = ({
  setSelectedImage,
  selectedImage,
}: RTFileUploadType) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const datasetInputRef = useRef<HTMLInputElement | null>(null);
  const [datasetUploaded, setDatasetUploaded] = useState<boolean>(false);
  const [isByColor, setIsByColor] = useState<boolean>(true);

  const handleChange: React.ChangeEventHandler<HTMLInputElement> | undefined = (
    e
  ) => {
    if (!e.target.files) return;
    const img = e.target.files[0];
    const reader = new FileReader();

    reader.addEventListener("load", () => {
      setSelectedImage(reader.result);
    });

    reader.readAsDataURL(img);
  };

  async function handleSubmit() {
    try {
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

      const data = await response.json();
      console.log(data);

      // Set datasetUploaded state based on the response
      setDatasetUploaded(true);
    } catch (error) {
      console.error("Error during fetch:", error);
    }
  }

  return (
    <div className="flex flex-col gap-8">
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
          <ToggleGroupDemo />
        </div>
      </div>
    </div>
  );
};

export default RTFileUpload;
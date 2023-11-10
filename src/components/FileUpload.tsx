"use client";
import React, { useRef, useState } from "react";

const CBIREndpoint = "http://localhost:8000/api/create-room";

type FileUploadType = {
  setSelectedImage: React.Dispatch<
    React.SetStateAction<string | ArrayBuffer | null>
  >;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
  selectedImage: string | ArrayBuffer | null;
};

const FileUpload = ({
  setSelectedImage,
  setLoading,
  selectedImage,
}: FileUploadType) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
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

      const formData = new FormData();
      formData.append("image", fileInputRef.current?.files[0] as File);

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
      <div className="flex flex-row items-center justify-between">
        <button className="flex cursor-pointer items-center justify-center rounded-md bg-[#57af95] px-4 py-2 font-thin text-white hover:bg-green-600">
          Upload dataset
        </button>
        {datasetUploaded && <p>Dataset uploaded!</p>}
      </div>
      <div className="flex-between flex flex-row">
        <p>Search by: </p>
        <button
          className="rounded bg-slate-600 py-2 text-white md:w-[100px] "
          onClick={handleSubmit}
        >
          Texture
        </button>
        <button
          className="rounded bg-slate-600 py-2 text-white md:w-[100px]"
          onClick={handleSubmit}
        >
          Color
        </button>
      </div>
    </div>
  );
};

export default FileUpload;

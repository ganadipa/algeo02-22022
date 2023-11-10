"use client";
import React, { useRef, type MouseEventHandler, useState } from "react";

const imgEndpoint = "http://localhost:8000/images/";

const FileUpload = () => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const createImage: MouseEventHandler<HTMLButtonElement> = async (e) => {
    e.preventDefault();
    if (!selectedImage) return;

    const formData = new FormData();
    formData.append("file", selectedImage);

    const newImage = await fetch(imgEndpoint, {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .catch((err) => {
        console.error(err);
      });
  };

  const handleChange: React.ChangeEventHandler<HTMLInputElement> | undefined = (
    e
  ) => {
    if (!e.target.files) return;
    const img = e.target.files[0];
    const reader = new FileReader();

    reader.addEventListener("load", () => {
      console.log(reader.result);
    });

    reader.readAsDataURL(img);
  };

  return (
    <div className="flex flex-col">
      <h2>Upload an image</h2>
      <input
        type="file"
        name=""
        id="imageInput"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleChange}
      />
      <button onClick={createImage}>submit</button>
    </div>
  );
};

export default FileUpload;

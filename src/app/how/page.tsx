import React from "react";

const Page = () => {
  return (
    <div className="max-w-[700px] rounded bg-white p-3 font-semibold md:text-xl">
      Content Based Image Retrieval is a problem of extracting certain aspects
      of a certain query image, and then traversing a sea of images (the
      dataset) to find and display similar ones. Here we have provided two
      modes: color-based and texture-based image searching. In color-based, our
      program will classify the colors of the image pixels into multiple
      channels (bins) and compares the channels of two images to determine
      similarity. Texture-based comparison on the other hand, is done by
      converting each image to a 3-length vector of contrast, homogeneity, and
      entropy values, and taking the similarity by comparing the vectors of
      images.
    </div>
  );
};

export default Page;

import React from "react";

const Page = () => {
  return (
    <div className="flex flex-wrap gap-8">
      <div className="max-w-[700px] rounded bg-white p-3 font-semibold ">
        For the main search (which is at /home), upload an image for query and
        upload a folder (dataset) which ALL inside the folder is a type of image
        is a MUST. For searching the similiarity between the query and each
        image in the dataset uploaded you can use search method by color or by
        texture.
      </div>
      <div className="max-w-[700px] rounded bg-white p-3 font-semibold">
        For the real time search, (which is at /realtime), you only need to
        upload a folder (dataset) which ALL inside the folder is a type of
        image.
        <br />
        As well as the main search you can also choose to search similiarities
        using its color or using its texture.
        <br />
        <br />
        By default, the search query will be automatically fetched if you dont
        lock the current preview image. So if you want to lock the previewed
        image, you have to lock it first by pressing the Lock button.
      </div>
    </div>
  );
};

export default Page;

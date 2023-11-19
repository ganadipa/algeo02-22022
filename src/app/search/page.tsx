import React from "react";

const Page = () => {
  return (
    <div className="flex justify-center flex-wrap gap-8">
      <div className="max-w-[700px] rounded bg-white p-3 font-semibold ">
        For the main search (which is at /home), upload an image as a query 
        and then upload a folder (dataset) which contains only images of 
        extensions .png, .jpg, or .jpeg. Wait a few moments before uploading 
        is done, and then you can simply click the "color" or the "texture" 
        button to search an image using the respective method.

      </div>
      <div className="max-w-[700px] rounded bg-white p-3 font-semibold">
        For the real time search, (which is at the /realtime page), you only 
        need to upload a folder (dataset) which contains images as well.
        <br />
        Like the main search you can also choose to search similiarities
        by color or by texture.
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

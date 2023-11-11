import { ProfileType } from "@/types";
import Image from "next/image";
import React from "react";

const TMP_NAME = "Nyoman Ganadipa Narayana";
const TMP_NIM = "13522066";
const TMP_DESC = "I love to do competitive programming";
const TMP_IMG = "/sunflower.jpg";
const ProfileCard = ({ name, description, img, nim }: ProfileType) => {
  return (
    <div className="flex aspect-[9/16] flex-col items-center justify-between gap-4 rounded-3xl bg-slate-50 p-4 pb-16 max-md:w-[180px] md:w-[300px]">
      <div className="relative aspect-square w-full rounded-full">
        <Image
          src={img}
          alt=""
          fill
          objectFit="cover"
          className="rounded-full"
        />
      </div>
      <h1>
        <strong>{name}</strong>/{nim}
      </h1>
      <p>{description}</p>
    </div>
  );
};

export default ProfileCard;

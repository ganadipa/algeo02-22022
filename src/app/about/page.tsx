import { AuthorProfiles } from "@/src/constant/about";
import ProfileCard from "@/src/components/ProfileCard";
import React from "react";

const Page = () => {
  return (
    <div className="flex flex-row flex-wrap items-center justify-center gap-16">
      {AuthorProfiles.map((profile) => (
        <ProfileCard
          key={profile.name}
          name={profile.name}
          description={profile.description}
          img={profile.img}
          nim={profile.nim}
        />
      ))}
    </div>
  );
};

export default Page;

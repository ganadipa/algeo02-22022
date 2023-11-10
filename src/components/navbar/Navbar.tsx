import { SignedIn, UserButton } from "@clerk/nextjs";
import Image from "next/image";
import Link from "next/link";
import React from "react";
import MobileNav from "./MobileNav";
import Theme from "./Theme";
const Navbar = () => {
  return (
    <nav className="flex-between background-light900_dark200 fixed z-50 w-full gap-5 p-4 shadow-light-300 dark:shadow-none sm:px-12">
      <Link href="/" className="flex items-center gap-2">
        <Image
          src={"/assets/images/site-logo.png"}
          width={23}
          height={23}
          alt=""
        />
        <p className="h2-bold font-spaceGrotesk text-dark-100 dark:text-light-900 max-sm:hidden">
          Gana&apos;s <span className="text-primary-500"> Box</span>
        </p>
      </Link>
      <div className="flex-between gap-5">
        <MobileNav />
      </div>
    </nav>
  );
};

export default Navbar;

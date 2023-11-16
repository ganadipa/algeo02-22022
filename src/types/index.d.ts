import React from "react";

export type FCChild = {
  children: React.ReactNode;
};

export interface SidebarLink {
  imgURL: string;
  route: string;
  label: string;
}
export type ProfileType = {
  name: string;
  nim: string;
  description: string;
  img: string;
};

export interface ParamsProps {
  params: { id: string };
}

export interface SearchParamsProps {
  searchParams: { [key: string]: string | undefined };
}

export interface URLProps {
  params: { id: string };
  searchParams: { [key: string]: string | undefined };
}

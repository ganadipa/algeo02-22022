import { SidebarLink } from "../types";

export const themes = [
  { value: "light", label: "Light", icon: "/assets/icons/sun.svg" },
  { value: "dark", label: "Dark", icon: "/assets/icons/moon.svg" },
  { value: "system", label: "System", icon: "/assets/icons/computer.svg" },
];

export const sidebarLinks: SidebarLink[] = [
  {
    imgURL: "/assets/icons/home.svg",
    route: "/",
    label: "Home",
  },
  {
    imgURL: "/assets/icons/about.svg",
    route: "/about",
    label: "About",
  },
  {
    imgURL: "/assets/icons/how.svg",
    route: "/how",
    label: "How It Works",
  },
  {
    imgURL: "/assets/icons/search.svg",
    route: "/search",
    label: "How To Use",
  },
  {
    imgURL: "/assets/icons/realtime.svg",
    route: "/realtime",
    label: "Real Time Experience",
  },
];

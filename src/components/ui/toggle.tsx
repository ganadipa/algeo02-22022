import React from "react";
import * as ToggleGroup from "@radix-ui/react-toggle-group";
import "./styles.css";

const ToggleGroupDemo = () => (
  <ToggleGroup.Root
    className="ToggleGroup"
    type="single"
    defaultValue="left"
    aria-label="Text alignment"
  >
    <ToggleGroup.Item
      className="ToggleGroupItem"
      value="left"
      aria-label="Left aligned"
    >
      Color
    </ToggleGroup.Item>

    <ToggleGroup.Item
      className="ToggleGroupItem"
      value="right"
      aria-label="Right aligned"
    >
      Texture
    </ToggleGroup.Item>
  </ToggleGroup.Root>
);

export default ToggleGroupDemo;

import React from "react";
import { apiMoofAction } from "./lookup";

export function ActionBtn(props) {
  const { moof, action, didPerformAction } = props;
  const likes = moof.likes ? moof.likes : 0;
  const className = props.className
    ? props.className
    : "btn btn-primary btn-sm";
  const actionDisplay = action.display ? action.display : "Action";
  const display =
    action.type === "like" ? `${likes} ${actionDisplay}` : actionDisplay;
  const handleActionBackendEvent = (response, status) => {
    console.log("response: ", response, "status:", status);
    if ((status === 200 || status === 201) && didPerformAction) {
      didPerformAction(response, status);
    }
  };
  const handleClick = (event) => {
    event.preventDefault();
    apiMoofAction(moof.id, action.type, handleActionBackendEvent);
  };
  return (
    <button className={className} onClick={handleClick}>
      {display}
    </button>
  );
}

import React from "react";
import { apiMoofCreate } from "./lookup";

export function MoofCreate(props) {
  const textAreaRef = React.createRef();
  const { didMoof } = props;
  const handleBackendUpdate = (response, status) => {
    if (status === 201) {
      didMoof(response);
    } else {
      console.log(response, status);
      alert("An error occured please try again.");
    }
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    const newVal = textAreaRef.current.value;
    // backend api request
    apiMoofCreate(newVal, handleBackendUpdate);
    textAreaRef.current.value = "";
  };
  return (
    <div className={props.className}>
      <form onSubmit={handleSubmit}>
        <textarea
          ref={textAreaRef}
          required={true}
          className="form-control"
          name="moof"
        ></textarea>
        <button type="submit" className="btn btn-primary my-3">
          Moof
        </button>
      </form>
    </div>
  );
}

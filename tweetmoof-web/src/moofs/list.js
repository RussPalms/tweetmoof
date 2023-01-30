import React, { useState, useEffect } from "react";
import { apiMoofList } from "./lookup";
import { Moof } from "./detail";

export function MoofsList(props) {
  const [moofsInit, setMoofsInit] = useState([]);
  const [moofs, setMoofs] = useState([]);
  const [nextUrl, setNextUrl] = useState(null);
  const [moofsDidSet, setMoofsDidSet] = useState(false);
  useEffect(() => {
    const final = [...props.newMoofs].concat(moofsInit);
    if (final.length !== moofs.length) {
      setMoofs(final);
    }
  }, [props.newMoofs, moofs, moofsInit]);
  useEffect(() => {
    if (moofsDidSet === false) {
      const handleMoofListLookup = (response, status) => {
        if (status === 200) {
          setNextUrl(response.next);
          setMoofsInit(response.results);
          setMoofsDidSet(true);
        }
        //else if (status === 201) {
        //console.log(response);
        //}
        else {
          console.log(status);
          alert("There was an error.");
        }
      };
      apiMoofList(props.username, handleMoofListLookup);
    }
  }, [moofsInit, moofsDidSet, setMoofsDidSet, props.username]);
  const handleDidRemoof = (newMoof) => {
    const updateMoofsInit = [...moofsInit];
    updateMoofsInit.unshift(newMoof);
    setMoofsInit(updateMoofsInit);
    const updateFinalMoofs = [...moofs];
    updateFinalMoofs.unshift(moofs);
    setMoofs(updateFinalMoofs);
  };

  const handleLoadNext = (event) => {
    event.preventDefault();
    if (nextUrl !== null) {
      const handleLoadNextResponse = (response, status) => {
        if (status === 200) {
          setNextUrl(response.next);
          const newMoofs = [...moofs].concat(response.results);
          setMoofsInit(newMoofs);
          setMoofs(newMoofs);
        }
      };
      apiMoofList(props.username, handleLoadNextResponse, nextUrl);
    }
  };

  return (
    <React.Fragment>
      {moofs.map((item, index) => {
        return (
          <Moof
            moof={item}
            didRemoof={handleDidRemoof}
            className="my-5 py-5 border-top border-bottom bg-white text-dark"
            key={`${index}-{item.id}`}
          />
        );
      })}
      {nextUrl !== null && (
        <button className="btn btn-outline-primary" onClick={handleLoadNext}>
          Load next
        </button>
      )}
    </React.Fragment>
  );
}

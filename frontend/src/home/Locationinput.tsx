import Button from "../layouts/Button";

import {getData} from "../apicall/api.ts"
import { useState } from "react";
type sentdata={
  start:string;
  end:string
}
type locprop={
  resdata:any;
}
function LocationInput({resdata}:locprop) {
  const[form,setform]=useState({
    start:"",
    end:""
    
  })
  const handleChange=(e:any)=>{
     setform({
      ...form,
      [e.target.name]:e.target.value
     })

   }







  const HandleSubmit=async (godata:sentdata):Promise<any> =>{
    try {
       const res=await getData(godata)
       console.log(res)
       resdata(res)
    } catch (error) {
      console.log(error)
    }         
  }
  
  return (
    <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-lg">
        <div className="text-center p-3">
        <h1 className="text-3xl font-bold text-gray-900">Find Your Route</h1>
        <p className="mt-2 text-gray-500">Enter your starting point and destination.</p>
        </div>
      <div className="flex flex-col gap-4">
        {/* From */}
        <div className="flex items-center gap-3">
          <span className="h-3 w-3 rounded-full bg-green-500"></span>

          <input
            type="text"
            placeholder="From: Bole, Mexico..."
            name="start"
            onChange={handleChange}
            className="flex-1 rounded-xl border border-gray-300 px-4 py-2 outline-none transition focus:border-green-500 focus:ring-2 focus:ring-green-200"
          />
        </div>

        {/* To */}
        <div className="flex items-center gap-3">
          <span className="h-3 w-3 rounded-full bg-red-500"></span>

          <input
            type="text"
            placeholder="To: 4 Kilo, Anfo..."
            name="end"
            onChange={handleChange}
            className="flex-1 rounded-xl border border-gray-300 px-4 py-2 outline-none transition focus:border-red-500 focus:ring-2 focus:ring-red-200"
          />
        </div>
      </div>
      <div className="flex flex-col gap-3 p-4">
      <Button text="use my location" style=" bg-green-500 hover:bg-green-400" ></Button>
       <Button text="Search route ->" style=" bg-red-500 hover:bg-red-400" onClick={()=>HandleSubmit(form)} ></Button>
     
      </div>
      {}

     

    </div>
     
  );
}

export default LocationInput;
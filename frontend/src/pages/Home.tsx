import LocationInput from "../home/Locationinput";
import Header from "../layouts/Header";
import Map from "../layouts/Map";
import { useState } from "react";
import RouteCard from "../layouts/RouteCard";


type bus={
  route_short_name:string;
  route_long_name:string;
}
function Home() {
  const [data,setData]=useState<any>({})
  const [selectedbus,setselectedbus]=useState<string>()

  const bus = data?.itineraries?.[0]?.legs;
  const felteredata=bus?.filter((item:bus)=> item.route_short_name===selectedbus)
  console.log(felteredata)


  return (
    <>
      <Header />

      <div className="mx-auto flex max-w-7xl flex-col gap-6 p-2 lg:flex-row">
        {/* Sticky sidebar on desktop */}
        <aside className="lg:sticky lg:top-4 lg:w-96 lg:self-start">
          <LocationInput resdata={setData} />
        </aside>

        {/* Main content */}
        <main className="flex-1">
          {/* Your map or route results go here */}
          {bus?.map((item:bus,index:number)=>{
            return <div  key={index} onClick={()=>setselectedbus(item?.route_short_name)}>
                 <RouteCard key={index}busNum={item?.route_short_name} name={item?.route_long_name} onselect={selectedbus===item.route_short_name} /></div>
          })}
          <Map data={felteredata}/>
        </main>
      </div>
    </>
  );
}

export default Home;
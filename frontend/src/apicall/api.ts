import axios from "axios"
type data={
    start:string;
    end:string;
}
export const getData=async (data:data):Promise<any>=>{
    try {
        const res= await axios.post("http://localhost:8000/find",data )
        return res.data
        
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
        
    }
 
}
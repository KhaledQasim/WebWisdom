import { signal } from "@preact/signals-react";
import axios from "axios";

const counter = signal(0);

const typed = signal("");
const domainResult = signal();



async function handleSubmit(e) {
  e.preventDefault();
  try {
  
    const response = await axios.post('http://localhost:8000/online', {
      data: typed.value,
    });
    console.log('Response:', response.data);
    domainResult.value = (JSON.stringify(response.data.data));
    console.log(domainResult.value);
    typed.value = "";
  } catch (error) {
    console.error(error);
  }
}


function DomainInput() {
  return (
    <div className="mb-24 mt-20 flex justify-center ">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type here"
          className="input input-bordered input-secondary w-full max-w-sm mx-2 md:max-w-lg lg:max-w-xl"
          onChange={(e) => (typed.value = e.target.value)}
          value={typed.value}
        />
        <button
          className="btn btn-primary w-16 m-2"
          type="submit"
          onClick={() => (counter.value += 1)}
        >
          Submit
        </button>
      </form>

  
      <div className="flex ml-5">{domainResult.value}</div>
    </div>
  );
}
export default DomainInput;

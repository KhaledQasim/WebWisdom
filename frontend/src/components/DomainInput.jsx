import { effect, signal } from '@preact/signals-react';
import axios from 'axios';

const counter = signal(0); 
const todo = signal();
const online = signal();

async function getTodo() {
  try {
    const response = await axios.get('http://localhost:8000/todo');
    todo.value = JSON.stringify(response.data);
    console.log(JSON.stringify(response.data));
  } catch (error) {
    console.error(error);
  }
}

async function getOnline() {
    try {
      const response = await axios.get('http://localhost:8000/online');
    //   online.value = JSON.stringify(response.data);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }


effect(() => {
    
    getOnline();
}); 


function DomainInput(){
    return(
        <div className="mb-24 mt-20 flex justify-center ">
            <input type="text" placeholder="Type here" className="input input-bordered input-secondary w-full max-w-sm mx-2 md:max-w-lg lg:max-w-xl" />
            <button className="btn btn-primary w-16" onClick={() => counter.value += 1}>{counter.value}</button>
            <div>
                {todo.value}
            </div>
        </div>
    );
}
export default DomainInput;
import DNS from "../assets/dns-clear.png";
import Keyboard from "../assets/key-clear.png";

function Steps() {
  return (
    <div className="grid grid-cols-1  md:grid-cols-2 gap-7 justify-items-center my-10 md:my-44">
      <div className="grid gap-y-2">
        <img alt="DNS" src={DNS} className="w-52 h-36 mx-auto md:w-56 md:h-44" />
        <div className="text-center text-primary text-2xl font-bold">Step One</div>
        <div className="text-center text-base-content text-lg">Confirm Domain Ownership</div>
      </div>
      <div className="grid gap-y-2">
        <img alt="Keyboard" src={Keyboard} className="w-42 h-40 mx-auto" />
        <div className="text-center text-primary text-2xl font-bold">Step Two</div>
        <div className="text-center text-base-content text-lg">Type Domain Below!</div>
      </div>
    </div>
  );
}

export default Steps;

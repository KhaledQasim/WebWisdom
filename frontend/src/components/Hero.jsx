import EyeLogo from "../assets/eye-clean.png";
import Pupil from "../assets/pupil.png";

const isMobile =
  /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|windows phone|playbook|silk|(android(?!.*mobile))/i.test(
    navigator.userAgent
  );

function pupilFollow() {
  /**
   * This function makes the pupil follow the cursor
   */
  document.addEventListener("mousemove", function (event) {
    // Follow mouse for pupil
    const eye = document.getElementById("Eye-Socket");
    const pupil = document.getElementById("pupil");
    

    const scaleFactor = 0.29;

    const eyeRect = eye.getBoundingClientRect();
    console.log(1,eyeRect.width);
    const eyeCenterX = eyeRect.left + eyeRect.width / 2;
    const eyeCenterY = eyeRect.top + eyeRect.height / 2;

    const angle = Math.atan2(
      event.clientY - eyeCenterY,
      event.clientX - eyeCenterX
    );
    const maxDistance = Math.min(eyeRect.width / 4, eyeRect.height / 4);
    const pupilX = scaleFactor * maxDistance * Math.cos(angle);
    const pupilY = scaleFactor * maxDistance * Math.sin(angle);

  
    pupil.style.transform = `translate(-44%,-70%) translate(${pupilX}px, ${pupilY}px)`;


  });
}

function pupilAutoMovement() {
  setTimeout(() => {
    const eye = document.getElementById("Eye-Socket");
    const pupil = document.getElementById("pupil");
    const pupilDot = document.getElementById("pupil-dot");
    const scaleFactor = 0.29;

    const eyeRect = eye.getBoundingClientRect();

    // Generate random values for pupil movement
    const randomAngle = Math.random() * 2 * Math.PI;
    const maxDistance = Math.min(eyeRect.width / 4, eyeRect.height / 4);
    const pupilX = scaleFactor * maxDistance * Math.cos(randomAngle);
    const pupilY = scaleFactor * maxDistance * Math.sin(randomAngle);

    pupil.style.transform = `translate(-44%,-70%) translate(${pupilX}px, ${pupilY}px)`;
    pupilDot.style.transform = `translate(-44%,-70%) translate(${pupilX}px, ${pupilY}px)`;
    requestAnimationFrame(pupilAutoMovement);
  }, 1000);
}
if (isMobile) {
  // Code for mobile devices
  pupilAutoMovement();
} else {
  // Code for laptops/desktops
  setTimeout(() => {
    pupilFollow();
  }, 500);
}
function Hero() {
  return (
    <div className="hero bg-base-100">
      <div className="hero-content w-screen max-w-[100vw] flex-col lg:flex-row-reverse">
        <div className="relative rounded-full" id="Eye-Socket">
          <img
            src={EyeLogo}
            alt="eye-logo"
            className="md:w-80 md:h-80 w-40 h-40 rounded-full"
          />

          <img
            id="pupil"
            src={Pupil}
            alt="Pupil"
            // transform -translate-x-1/2 -translate-y-1/2
            className="md:w-[4.5rem] md:h-[4.5rem] w-9 h-9 absolute top-1/2 left-1/2 translate-x-[-44%] translate-y-[-70%] rounded-full"
          />
         
        </div>
        <div className="space-y-5">
          <h1 className="text-5xl font-bold  tracking-normal ">
            Guarding Your Digital Fortress!
          </h1>

          <p className="py-6 tracking-tight ">
            WebWisdom is a straight forward security scanner for your online
            websites, all it takes is two simple steps
          </p>
        </div>
      </div>
    </div>
  );
}

export default Hero;

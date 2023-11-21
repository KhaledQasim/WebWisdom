import EyeLogo from "../assets/oig-clean.png";
import Pupil from "../assets/white.png";

const isMobile =
  /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|windows phone|playbook|silk|(android(?!.*mobile))/i.test(
    navigator.userAgent
  );

function pupilFollow() {
  /**
   * This function makes the pupil follow the cursor
   */
  const eye = document.getElementById("Eye-Socket");
  const pupil = document.getElementById("pupil");
  const scaleFactor = 0.15;
  const eyeRect = eye.getBoundingClientRect();

  const eyeCenterX = eyeRect.left + eyeRect.width / 2;
  const eyeCenterY = eyeRect.top + eyeRect.height / 2;
  const maxDistance = Math.min(eyeRect.width / 4, eyeRect.height / 4);
  document.addEventListener("mousemove", function (event) {
    // Follow mouse for pupil

    const angle = Math.atan2(
      event.clientY - eyeCenterY,
      event.clientX - eyeCenterX
    );

    const pupilX = scaleFactor * maxDistance * Math.cos(angle);
    const pupilY = scaleFactor * maxDistance * Math.sin(angle);

    pupil.style.transform = `translate(-50%,-66%) translate(${pupilX}px, ${pupilY}px)`;
  });
}

// function angle(cx, cy, ex, ey) {
//   const dy = ey - cy;
//   const dx = ex - cx;
//   const rad = Math.atan2(dy, dx);
//   const deg = rad * (180 / Math.PI);
//   return deg;
// }

// function pupilFollow2() {
//   const eye = document.getElementById("Eye-Socket");
//   const pupil = document.getElementById("pupil");

//   const eyeRect = eye.getBoundingClientRect();

//   const eyeCenterX = eyeRect.left + eyeRect.width / 2;
//   const eyeCenterY = eyeRect.top + eyeRect.height / 2;

//   document.addEventListener("mousemove", function (event) {
//     // Follow mouse for pupil

//     const mouseX = event.clientX;
//     const mouseY = event.clientY;

//     const angleDeg = angle(mouseX, mouseY, eyeCenterX, eyeCenterY);

//     pupil.style.transform = `rotate(${180+angleDeg}deg))`;
//   });
// }

function pupilAutoMovement() {
  setTimeout(() => {
    const eye = document.getElementById("Eye-Socket");
    const pupil = document.getElementById("pupil");

    const scaleFactor = 0.15;

    const eyeRect = eye.getBoundingClientRect();

    // Generate random values for pupil movement
    const randomAngle = Math.random() * 2 * Math.PI;
    const maxDistance = Math.min(eyeRect.width / 4, eyeRect.height / 4);
    const pupilX = scaleFactor * maxDistance * Math.cos(randomAngle);
    const pupilY = scaleFactor * maxDistance * Math.sin(randomAngle);

    pupil.style.transform = `translate(-50%,-66%) translate(${pupilX}px, ${pupilY}px)`;

    requestAnimationFrame(pupilAutoMovement);
  }, 700);
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
            className="md:w-7 md:h-16 w-3 h-9 absolute top-1/2 left-1/2  translate-x-[-50%] translate-y-[-66%] rounded-full"
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

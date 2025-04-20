import image1 from "../../../public/images/resourceimage1.svg"
import image2 from "../../../public/images/resourceimage2.svg"
import image3 from "../../../public/images/resourceimage3.svg"
import image4 from "../../../public/images/resourceimage4.svg"



export default function Resources() {
  return (
    <section id="resources" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4">

        {/* Headline */}
        <h2 className="text-center text-3xl md:text-4xl font-bold mb-4 leading-tight text-black">
          Backed by <span className="text-gray-500">Amazing <br />
           Investor </span> In Our Mission <br /> To Help Teams Everywhere.
        </h2>

        {/* Investor Logos */}
        <div className="flex justify-center gap-6 md:gap-8 mt-8 mb-16 flex-wrap">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="w-16 h-16 md:w-20 md:h-20 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">aIx</span>
            </div>
          ))}
        </div>

        {/* Grid Content */}
        <div className="grid md:grid-cols-2 gap-12 items-center">

          {/* Left Block */}
          <div>
            <h3 className="text-2xl font-bold mb-4 text-black">Book. Manage. Optimize.</h3>
            <p className="text-gray-700 mb-4 leading-relaxed">
              Atlas gives your team the power to reserve desks, meeting rooms, or event spaces in just a few clicks.
              No lift. Atlas, your team can browse available desks, meeting rooms, or event spaces in real time—then book in just a few clicks.
            </p>
            <p className="text-gray-700 mb-4 leading-relaxed">
              Everything updates instantly, so your workspace runs like clockwork.
            </p>
            <ul className="text-gray-700 space-y-2 mb-6">
              <li>🔹 Book without hassle</li>
              <li>🔹 Modify or cancel with ease</li>
              <li>🔹 Real-time availability, always accurate, no guesswork.</li>
            </ul>
            <button className="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700 transition">
              Try Atlas Free
            </button>
          </div>

          {/* Right Image */}
          <div>
            <img
              src={image1.src}
              alt="Workspace Booking Illustration"
              className="rounded shadow-lg w-full object-cover"
            />
          </div>

          {/* Left Image */}
          <div className="md:order-2">
            <img
              src={image2.src}
              alt="Office Space Example"
              className="rounded shadow-lg w-full object-cover"
            />
          </div>

          {/* Right Block */}
          <div className="md:order-3">
            <h3 className="text-2xl font-bold mb-4 text-black">Designed for Real Workplaces</h3>
            <p className="text-gray-700 mb-4 leading-relaxed">
              Whether you're managing hundreds of employees or a handful of rotating learners,
              Atlas scales to meet your needs.
            </p>
            <ul className="text-gray-700 space-y-2">
              <li>✅ Live availability views</li>
              <li>✅ Custom user roles (Admin, Employee, Learner)</li>
              <li>✅ Automated reminders and smart alerts</li>
              <li>✅ Flexible bookings — on-site or remote</li>
              <li>✅ In-depth analytics to drive smart decisions</li>
            </ul>
          </div>


          {/* Left Block */}
          <div className="md:order-3">
            <h3 className="text-2xl font-bold mb-4 text-black">Safe. Secure. Seamless</h3>
            <p className="text-gray-700 mb-4 leading-relaxed">
            Your data is protected with enterprise-grade encryption and authentication. <br />
            Atlas is fully compliant and designed for peace of mind—whether you're managing sensitive meetings or public events.
            </p>
          </div>

          <div className="md:order-3">
            <img
              src={image3.src}
              alt="Workspace Booking Illustration"
              className="rounded shadow-lg w-full object-cover"
            />
          </div>

          <div className="md:order-3">
            <img
              src={image4.src}
              alt="Workspace Booking Illustration"
              className="rounded shadow-lg w-full object-cover"
            />
          </div>

             {/* Right Block */}
             <div className="md:order-3">
            <h3 className="text-2xl font-bold mb-4 text-black">Insights That Power Better Decisions</h3>
            <p className="text-gray-700 mb-4 leading-relaxed">
            Atlas gives Admins the visibility they need to make spaces work harder.
            </p>
            <ul className="text-gray-700 space-y-2">
              <li>✅ Usage reports across all workspaces</li>
              <li>✅ Occupancy trends and peak booking hours</li>
              <li>✅ Actionable insights to reduce waste and optimize layout</li>
            </ul>
          </div>


        </div>
      </div>
    </section>
  );
}

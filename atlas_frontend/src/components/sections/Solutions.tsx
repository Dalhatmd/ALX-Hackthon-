import {
  FaSlack,
  FaGoogle,
  FaCalendarAlt,
  FaStripe,
  FaMicrosoft,
} from "react-icons/fa";
import { SiGooglemeet } from "react-icons/si";
import { AiOutlineMail as AiMail } from "react-icons/ai";

export default function Solutions() {
  return (
    <section
      className="min-h-screen bg-gradient-to-r from-pink-50 via-pink-100 to-purple-100 px-8 py-16 flex items-center justify-center"
    >
      <div className="max-w-7xl w-full grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        {/* Left: Text Section */}
        <div>
          <span className="inline-block bg-gray-200 text-gray-700 text-xs tracking-widest uppercase px-3 py-1 rounded-full mb-4">
            Integrations
          </span>
          <h2 className="text-3xl md:text-4xl font-extrabold text-gray-900 leading-tight mb-6">
            Seamlessly Connect Atlas <br />
            With The Tools You Already Use
          </h2>
          <p className="text-gray-700 text-base leading-relaxed max-w-md">
            Easily integrate Atlas into your existing workflow whether it's
            collaboration platforms, calendar tools, or secure authentication
            systems. From Google Workspace and Microsoft 365 to SAML SSO and
            beyond, Atlas fits right into your ecosystem without friction.
          </p>
        </div>

        {/* Right: Icons and CTA */}
        <div className="relative h-full flex flex-col items-center justify-between">
          {/* Icons Grid */}
          <div className="grid grid-cols-3 gap-8 mb-16">
            <FaSlack size="2.5rem" color="#4A154B" />
            <FaGoogle size="2.5rem" color="#4285F4" />
            <SiGooglemeet size="2.5rem" color="#00897B" />
            <FaCalendarAlt size="2.5rem" color="#1A73E8" />
            <FaMicrosoft size="2.5rem" color="#5E5E5E" />
            <FaStripe size="2.5rem" color="#635BFF" />
            <AiMail size="2.5rem" color="#0072C6" />
          </div>

          {/* CTA Section */}
          <div className="text-center">
            <h3 className="text-2xl font-semibold text-indigo-600 mb-2">
              Lets get started
            </h3>
            <p className="text-sm text-gray-700 max-w-xs mx-auto">
              Join teams that are already transforming how they work with Atlas.
              Whether you're booking one room or a hundred, it all starts here.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

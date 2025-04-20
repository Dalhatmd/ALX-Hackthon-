import HeroImage from "../../../public/images/heroimage.svg"

export default function Hero() {
  return (
    <section
      id="hero"
      className="flex items-center justify-center min-h-screen bg-gradient-to-r from-pink-100 via-white to-purple-100 text-center px-4"
    >
      <div className="max-w-3xl">

        {/* Subheading Right Aligned */}
        <p className="text-md text-gray-700 mb-8 md:text-center pt-20">
          Atlas makes workspace management effortless.
        </p>
        
        {/* Search Bar */}
        <div className="flex justify-center mb-10">
          <div className="flex items-center bg-white shadow-md rounded-full px-6 py-3 w-full max-w-lg">
            <input
              type="text"
              placeholder="Search for available desks, meeting rooms, event spaces"
              className="flex-grow text-gray-500 placeholder-gray-400 focus:outline-none"
            />
            <svg className="w-5 h-5 text-gray-400 ml-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M12.9 14.32a8 8 0 111.414-1.414l4.387 4.386a1 1 0 01-1.414 1.415l-4.387-4.387zM8 14a6 6 0 100-12 6 6 0 000 12z" clipRule="evenodd" />
            </svg>
          </div>
        </div>

        {/* Heading */}
        <h1 className="text-black text-6xl md:text-7xl font-bold leading-tight mb-4">
          Book It. 
          Use It. <br />
          Love It.
        </h1>

        {/* Paragraph */}
        <p className="text-base text-gray-600 mb-8 max-w-2xl mx-auto">
          Whether you're a growing company or a dynamic learning institution, Atlas helps you streamline workspace bookings, boost space efficiency, and keep everyone in sync without the chaos.
        </p>

        {/* Buttons */}
        <div className="flex justify-center space-x-4">
          <button className="bg-purple-600 text-white py-2 px-6 rounded hover:bg-purple-700 transition cursor-pointer">
            Demo book
          </button>
          <button className="bg-white border border-gray-300 text-gray-700 py-2 px-6 rounded hover:bg-gray-100 transition cursor-pointer">
            Explore Pricing
          </button>
        </div>

        {/* Image */}
        <div className="flex justify-center mt-8">
          <img
            src={HeroImage.src}
            alt="Hero Section Image"
            width="1842"
            height="800"
            className="rounded-lg shadow-md"
          />
        </div>
      </div>
    </section>
  );
}

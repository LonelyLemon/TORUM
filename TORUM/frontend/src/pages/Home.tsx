const Home: React.FC = () => {
    return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] bg-gradient-to-b from-blue-50 to-white p-4">
        <div className="max-w-3xl text-center">
            <h1 className="text-4xl font-extrabold text-blue-800 mb-6">Welcome to TORUM</h1>
            <p className="text-lg text-gray-700">
            TORUM - A forum where traders can communicate and share about trading experiences,
            trading signals, trading systems, and financial knowledge, with various functionalities
            such as book area, document area and more.
            </p>
        </div>
        <div className="grid grid-cols-1 gap-6 mt-10 w-full max-w-4xl md:grid-cols-3">
            <div className="p-6 bg-white rounded-lg shadow">
                <h2 className="mb-2 text-xl font-semibold">Join Discussions</h2>
                <p className="text-sm text-gray-600">Connect with other traders in real-time forums.</p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow">
                <h2 className="mb-2 text-xl font-semibold">Share Knowledge</h2>
                <p className="text-sm text-gray-600">Upload documents and trading books to help the community grow.</p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow">
                <h2 className="mb-2 text-xl font-semibold">Stay Updated</h2>
                <p className="text-sm text-gray-600">Follow the latest trading signals and system updates.</p>
            </div>
        </div>
    </div>
  );
};

export default Home;
import { Navbar } from "../components/Navbar";
import { StyleGrid } from "../components/StyleGrid";

const Index = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto py-8">
        <StyleGrid />
      </main>
    </div>
  );
};

export default Index;
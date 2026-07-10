import LocationInput from "../home/Locationinput";
import Header from "../layouts/Header";

function Home() {
  return (
    <>
      <Header />

      <div className="mx-auto flex max-w-7xl flex-col gap-6 p-2 lg:flex-row">
        {/* Sticky sidebar on desktop */}
        <aside className="lg:sticky lg:top-4 lg:w-96 lg:self-start">
          <LocationInput />
        </aside>

        {/* Main content */}
        <main className="flex-1">
          {/* Your map or route results go here */}
        </main>
      </div>
    </>
  );
}

export default Home;
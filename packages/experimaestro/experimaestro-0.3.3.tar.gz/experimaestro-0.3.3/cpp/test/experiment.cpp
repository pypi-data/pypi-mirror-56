// Fake experiment -- useful to run tests

#include <thread>

#include <Poco/Path.h>
#include <xpm/common.hpp>
#include <xpm/cpp.hpp>
#include <xpm/logging.hpp>
#include <xpm/rpc/server.hpp>
#include <xpm/workspace.hpp>
#include <xpm/xpm.hpp>

#include <__xpm/CLI11.hpp>
#include <__xpm/common.hpp>


using namespace xpm;
DEFINE_LOGGER("xpm");

struct TypeA : public CppObject<TypeA> {
  bool failure;
  long sleep;
  std::shared_ptr<TypeA> parent;

  void run() override {
    std::cerr << "Running !!!\n";
    std::chrono::seconds duration(sleep);

    size_t N = 100;
    for(size_t i = 0; i < N; ++i) {
      std::this_thread::sleep_for(duration / 100.);
      progress((float)i / (float)N);
    }    

    if (failure) throw std::runtime_error("failed as you wished");
  }

};

XPM_TYPE("TypeA", TypeA)
    .argument("sleep", &TypeA::sleep)
    .argument("failure", &TypeA::failure)
    .argument("parent", &TypeA::parent).required(false);
XPM_SIMPLETASK("task.a", TypeA);

int main(int argc, const char **argv) {

  if (argc > 1 && argv[1] == std::string("run")) {
    return currentRegister()->parse(argc, argv) ? 0 : 1;
  }
   
  CLI::App app{"Fake experiments"};
  app.require_subcommand(1);
  app.fallthrough(false);
  *EXECUTABLE_PATH = Path(Poco::Path(argv[0]).absolute().toString());

  {
    std::string workdir;
    int port;

    auto _run = app.add_subcommand("xp", "Run the experiment");
    _run->add_option("--port", port, "The working directory");
    _run->add_option("workdir", workdir, "The working directory")
        ->required(true);

      

    _run->set_callback([&]() {
      auto ws = mkptr<Workspace>(workdir);
      ws->experiment("test");
      auto launcher = Launcher::defaultLauncher();
      if (port > 0) {
        auto server = ws->server(port, ".");
        launcher->notificationURL(server->getNotificationURL());
      }
      
      // Will always be empty
      std::vector<std::shared_ptr<Dependency>> dependencies;

      for(int a: {1, 5, 30, 60, 120, 240}) {
        auto v = Value::create(
                    *currentRegister(),
                    {{"$type", "TypeA"}, {"sleep", a}, {"failure", false}})
                    ->asMap();

        v->addTag("sleep", a);


        currentRegister()
            ->getTask(Typename("task.a"))
            ->submit(ws, launcher, v, dependencies);

        auto v2 = Value::create(*currentRegister(),
          {{"$type", "TypeA"}, {"sleep", a}, {"failure", false}})
        ->asMap();
        v2->set("parent", v);
        v2->addTag("dep", true);

        currentRegister()
            ->getTask(Typename("task.a"))
            ->submit(ws, launcher, v2, dependencies);
      }
      Workspace::waitUntilTaskCompleted();
    });
  }


  CLI11_PARSE(app, argc, argv);
}
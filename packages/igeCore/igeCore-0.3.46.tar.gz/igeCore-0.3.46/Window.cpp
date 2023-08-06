#include "pyxie.h"
#include "Window.h"
#include <python.h>
#include <thread>
#include <mutex>

#include "pyxieApplication.h"
#include "pyxieFios.h"
#include "pyxieTouchManager.h"
#include "pyxieResourceManager.h"
#include "pyxieRenderContext.h"
#include "pyxieShader.h"
#include "pyxieSystemInfo.h"
#include "Backyard.h"

class TestApp : public pyxie::pyxieApplication
{
public:
	TestApp() {
		
		pyxie::pyxieFios::Instance().SetRoot();
	}
	~TestApp() {}

	bool onInit(DeviceHandle dh) {
		if (pyxieApplication::onInit(dh) == false) return false;
		pyxie::Backyard::New();
		return true;
	}
	void onShutdown() {
		pyxie::Backyard::Delete();
		pyxieApplication::onShutdown();
	}
	bool onUpdate(){
		pyxie::Backyard::Instance().SyncMain();
		if (pyxieApplication::onUpdate() == false) return false;
		return true;
	}
	void onRender(){
		//pyxie::Backyard::Instance().Render();
	}
};

extern std::shared_ptr<pyxie::pyxieApplication> gApp = std::make_shared<TestApp>();

void pyxieShowWindow(bool show, int width, int height, bool resizable) {
	gApp->showAppWindow(show, width, height, resizable);
}

void CreateApplication() {
	gApp->createAppWindow(true);
}

PyMODINIT_FUNC _PyInit__igeCore();

PyMODINIT_FUNC PyInit__igeCore() {
	CreateApplication();
	return _PyInit__igeCore();
}


///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include <memory>

#include "pyxieEvent.h"
#include "pyxieMathutil.h"

namespace pyxie
{
    class Finger;
    
    class PYXIE_EXPORT TouchEvent : public Event
    {
    public:       
        enum class EventCode
        {
            BEGAN,
            MOVED,
            ENDED,
            SCROLLED
        };
        
        TouchEvent(EventCode eventCode, std::shared_ptr<Finger> finger);
        virtual ~TouchEvent();

        EventCode getEventCode() const;
        std::shared_ptr<Finger> getFinger() const;

    protected:
        EventCode _eventCode;
        std::shared_ptr<Finger> _finger;       

        friend class TouchEventListener;
    };

    class PYXIE_EXPORT TouchEventListener: public EventListener
    {
    public:
        TouchEventListener();
        virtual ~TouchEventListener();
        virtual bool init();

        void setOnTouchBeganCallback(std::function<void(std::shared_ptr<Event> event)> fn);
        void setOnTouchEndedCallback(std::function<void(std::shared_ptr<Event> event)> fn);
        void setOnTouchMovedCallback(std::function<void(std::shared_ptr<Event> event)> fn);
        void setOnTouchScrolledCallback(std::function<void(std::shared_ptr<Event> event)> fn);

    protected:
        std::function<void(std::shared_ptr<Event> event)> onTouchBegan;
        std::function<void(std::shared_ptr<Event> event)> onTouchEnded;
        std::function<void(std::shared_ptr<Event> event)> onTouchMoved;
        std::function<void(std::shared_ptr<Event> event)> onTouchScrolled;        

        friend class TouchEvent;
    };

    class PYXIE_EXPORT Finger
    {
        enum class FingerState: uint16_t
        {
            FREE = 0,                
            PRESSED,
            MOVED,
            RELEASED,
            SCROLLED
        };

    public:
        Finger(uint32_t fingerId);
        virtual ~Finger();        
        void clearFinger();

        bool isPressed() const;
        bool isMoved() const;
        bool isReleased() const;
        bool isScrolled() const;

        void setFingerId(uint32_t id);
        uint32_t getFingerId() const;
        uint16_t getFingerState() const;       
        float getCurrentPosX() const;
        float getCurrentPosY() const;
        float getPressure() const;
        
        Vec2 getStartPoint() const;
        Vec2 getCurrentPoint() const;   
        Vec2 getPreviousPoint() const;     

        float getScrollX() const;
        float getScrollY() const;
        bool isScrollFlipped() const;

        void update(TouchEvent::EventCode eventCode, float x, float y, float pressure);
        void updateState();

    protected:
        uint32_t _fingerId;
        Vec2 _point;        
        float _pressure;
        
        Vec2 _startPoint;
        Vec2 _prevPoint;
        bool _startPointCaptured;

        float _scrollX;
        float _scrollY;
        bool _scrollFlipped;

        uint16_t _fingerState;
    };

    class PYXIE_EXPORT TouchDevice
    {
    public:
        TouchDevice();
        virtual ~TouchDevice();

        void setEventDispatcher(std::shared_ptr<EventDispatcher> dispatcher);
        void update();

        bool isFingerPressed(uint32_t fingerId);
        bool isFingerMoved(uint32_t fingerId);
        bool isFingerReleased(uint32_t fingerId);
        bool isFingerScrolled(uint32_t fingerId);
        
        void getFingerPosition(uint32_t fingerId, float& posX, float& posY);
        float getFingerPressure(uint32_t fingerId);
        void getFingerScrolledData(uint32_t fingerId, float& scroll_x, float& scroll_y, bool& isInverse);

        int getFingersCount();
        std::vector<std::shared_ptr<Finger>>& getAllFingers();

        void dispatchTouchEvent(TouchEvent::EventCode eventCode, uint32_t fingerId, float x, float y, float pressure);

    protected:
        int addFinger(uint32_t fingerID);
        void removeFinger(uint32_t fingerID);
        int getFingerIndex(uint32_t fingerId);

        std::shared_ptr<EventDispatcher> mEventDispatcher;
        std::vector<std::shared_ptr<Finger>> _fingers;
    };
}

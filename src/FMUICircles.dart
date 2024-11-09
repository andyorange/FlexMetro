import 'package:flutter/material.dart';

class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  int selectedCircle = 0; // Index of the selected circle
  bool isBlinking = false; // Flag to track if a circle is currently blinking

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Blinking Circles'),
      ),
      body: Center(
        child: Stack(
          children: [
            // Circle 1
            AnimatedOpacity(
              opacity: selectedCircle == 0 ? (isBlinking ? 0.2 : 1.0) : 1.0,
              duration: Duration(milliseconds: 100),
              child: Container(
                width: 100,
                height: 100,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.yellow,
                ),
              ),
            ),
            // Circle 2
            AnimatedOpacity(
              opacity: selectedCircle == 1 ? (isBlinking ? 0.2 : 1.0) : 1.0,
              duration: Duration(milliseconds: 100),
              child: Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.blue,
                ),
              ),
            ),
            // Circle 3
            AnimatedOpacity(
              opacity: selectedCircle == 2 ? (isBlinking ? 0.2 : 1.0) : 1.0,
              duration: Duration(milliseconds: 100),
              child: Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.cyan,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void tickCallback(int selectedCircle) {
    setState(() {
      this.selectedCircle = selectedCircle;
      isBlinking = true;
      Future.delayed(Duration(milliseconds: 100), () {
        isBlinking = false;
      });
    });
  }
}

class AnimatedOpacity extends StatefulWidget {
  final double opacity;
  final Duration duration;
  final Widget child;

  AnimatedOpacity({
    required this.opacity,
    required this.duration,
    required this.child,
  });

  @override
  _AnimatedOpacityState createState() => _AnimatedOpacityState();
}

class _AnimatedOpacityState extends State<AnimatedOpacity>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: widget.duration,
      vsync: this,
    );
    _animation = Tween<double>(begin: 0.0, end: widget.opacity).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ),
    );
    _controller.addListener(() {
      setState(() {});
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Opacity(
          opacity: _animation.value,
          child: widget.child,
        );
      },
    );
  }
}
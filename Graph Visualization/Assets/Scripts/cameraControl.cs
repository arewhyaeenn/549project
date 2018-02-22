using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// camera controls:
// 	initially in control scheme 1, press Tab to switch
// 	control scheme 1 (WASD): wasdqe --> forward left back right up down respectively
//			mouse --> turn
// 	TODO: control scheme 2 2 (drag): right click and drag to move in plane perpendicular to forward
//			scroll to move forward / backward
//			after basic objects are made, allow for zoom on current selection


public class CameraControl : MonoBehaviour
{

	private float speed = 5f; // move speed
	private Vector3 lookRot = Vector3.zero; // look rotation
	private float sensitivity = 120f; // turn speed
	private bool mode = true; // control scheme switch
	private CharacterController con; // for smooth movement
	// TODO allow user to change speed / sensitivity through interface
	// TODO save user settings (JSON?) for easy import

	void Start ()
	{
		con = GetComponent<CharacterController> ();
	}

	void Update ()
	{

		// switch camera mode
		if (Input.GetKeyDown (KeyCode.Tab))
		{
			mode = !mode;
		}

		// get player input based on control mode
		if (mode)
		{
			WASD ();
		}
		else
		{
			drag ();
		}
	}


	// TODO add axis for roll?
	// one of the above, power or ease?
	void WASD ()
	{

		Vector3 dir = Vector3.zero; // placeholder vector for rotation and movement

		// get mouse movement
		float mouseX = Input.GetAxis ("Mouse X");
		float mouseY = -Input.GetAxis ("Mouse Y");

		// rotate camera
		lookRot.y += mouseX * sensitivity * Time.deltaTime;
		lookRot.x += mouseY * sensitivity * Time.deltaTime;

		// bound lookRot.x to prevent flipping
		lookRot.x = Mathf.Clamp(lookRot.x, -90f, 90f);

		// rotate camera
		transform.rotation = Quaternion.Euler(lookRot);

		// reset dir
		dir = Vector3.zero;

		// get horizontal movement input
		dir += Input.GetAxis("Horizontal") * transform.right;

		// " forward "
		dir += Input.GetAxis("Vertical") * transform.forward;

		// " vertical "
		dir += Input.GetAxis("QandE") * transform.up;

		// set direction length to 1
		dir.Normalize();

		// move camera
		con.Move(dir * speed * Time.deltaTime);
	}

	void drag ()
	{

	}
}

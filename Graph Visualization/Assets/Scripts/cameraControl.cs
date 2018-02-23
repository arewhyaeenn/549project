using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// camera controls:
// 	initially in control scheme 1, press Tab to switch
// 	control scheme 1 (WASD): wasdqe --> forward left back right up down respectively
//			mouse --> turn
// 	TODO: control scheme 2 (drag): right click and drag to turn
//			middle click and drag to move in plane perpendicular to forward
//			scroll to move forward / backward
//			after basic objects are made, allow for zoom on
//  TODO allow user to change speed / sensitivity through interface
//  TODO save user settings (JSON?) for easy import


public class CameraControl : MonoBehaviour
{
	private Vector3 lookRot = Vector3.zero; // look rotation
	private bool mode = true; // control scheme switch
	private CharacterController con; // for smooth movement
	private float sensitivity = 120f; // turn speed

	private float speed = 5f; // move speed for WASD

	// params for drag mode
	private float dragSpeed = 5f;
	private bool isDragging = false;
	private bool isTurning = false;

	// params for selection tracking
	private List<Vertex> V = new List<Vertex> ();
	private List<Edge> E = new List<Edge> ();


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
		// left click
		if (Input.GetMouseButtonDown (0))
		{
			// clicked on object
			RaycastHit hit;
			Ray ray = Camera.main.ScreenPointToRay (Input.mousePosition);
			if (Physics.Raycast (ray, out hit, 1 << 8 | 1 << 9)) // layer 8 is Vertex, 9 is Edge
			{
				// clicked on vertex
				if (hit.collider.gameObject.layer == 8)
				{
					Vertex vertex = hit.collider.GetComponent<Vertex> ();
					if (Input.GetKey (KeyCode.LeftShift))
					{
						vertex.ToggleSelected ();
						if (vertex.isSelected)
						{
							V.Add (vertex);
							Debug.Log (V.Count);
						}
						else
						{
							V.Remove (vertex);
							Debug.Log (V.Count);
						}
					}
					else
					{
						this.EmptySelected ();
						V.Add (vertex);
						vertex.SetSelected (true);
						Debug.Log (V.Count);
					}
				}
				// clicked on edge
				else if (hit.collider.gameObject.layer == 9)
				{
					Edge edge = hit.collider.GetComponent<Edge> ();
					if (Input.GetKey (KeyCode.LeftShift))
					{
						edge.ToggleSelected ();
						if (edge.isSelected)
						{
							E.Add (edge);
							Debug.Log (E.Count);
						}
						else
						{
							E.Remove (edge);
							Debug.Log (E.Count);
						}
					}
					else
					{
						this.EmptySelected ();
						E.Add (edge);
						edge.SetSelected (true);
						Debug.Log (E.Count);
					}
				}
			}
			else
			{
				if (!Input.GetKey (KeyCode.LeftShift))
				{
					this.EmptySelected ();
				}
				Debug.Log (V.Count);
				Debug.Log (E.Count);
			}
		}

		// right click
		else if (Input.GetMouseButtonDown (1))
		{
			Debug.Log ("Right Click");
		}

		// middle click or left control
		else if (Input.GetMouseButtonDown (2))
		{
			Debug.Log ("Middle Click");
		}
	}


	void EmptySelected ()
	{
		int index = V.Count - 1;
		while (index >= 0)
		{
			V [index].SetSelected (false);
			V.RemoveAt (index);
			index--;
		}

		index = E.Count - 1;
		while (index >= 0)
		{
			E [index].SetSelected (false);
			E.RemoveAt (index);
			index--;
		}
	}
}

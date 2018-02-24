﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// camera controls:
// 	initially in control scheme 2, press Tab to switch
// 	control scheme 1 (WASD): wasdqe --> forward left back right up down respectively
//			mouse --> turn
// 	control scheme 2 (drag): right click and drag to turn
//			middle click and drag to move in plane perpendicular to forward
//			scroll to move forward / backward
//			TODO if objects are selected, scroll to scale distance from centroid
//  TODO allow user to change speed / sensitivity through interface
//  TODO save user settings (JSON?) for easy import
//	TODO delete control scheme 1, it was nice to use while testing parts of 2 though

public class CameraControl : MonoBehaviour
{
	private Vector3 lookRot = Vector3.zero; // look rotation
	private bool mode = false; // control scheme switch
	private CharacterController con; // for smooth movement
	private float sensitivity = 120f; // turn speed
	private float camClampAngle = 80f;

	private float speed = 5f; // move speed for WASD

	// params for drag mode
	private float moveSpeed = 5f;
	private float scrollSpeed = 5f;
	private bool isDragging = false; // moving selected objects
	private bool isTurning = false; // turning camera
	private bool isSelecting = false; // selecting objects
	private bool isMoving = false; // moving camera

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

		// get mouse movement
		float mouseX = Input.GetAxis ("Mouse X");
		float mouseY = -Input.GetAxis ("Mouse Y");
		lookRot.y += mouseX * sensitivity * Time.deltaTime;
		lookRot.x += mouseY * sensitivity * Time.deltaTime;

		// clamp to prevent flipping
		lookRot.x = Mathf.Clamp(lookRot.x, -camClampAngle, camClampAngle);

		// rotate camera
		transform.rotation = Quaternion.Euler(lookRot);

		// get horizontal movement input
		Vector3 dir = Input.GetAxis("Horizontal") * transform.right;

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
		// let go of left click
		if (Input.GetMouseButtonUp (0))
		{
			isSelecting = false;
		}

		// let got of right click
		if (Input.GetMouseButtonUp (1))
		{
			isTurning = false;
		}

		// let got of middle click
		if (Input.GetMouseButtonUp (2))
		{
			isMoving = false;
		}

		if (!(isTurning || isMoving))
		{
			// left click
			if (Input.GetMouseButtonDown (0))
			{
				// clicked on object
				RaycastHit hit;
				Ray ray = Camera.main.ScreenPointToRay (Input.mousePosition);
				if (Physics.Raycast (ray, out hit, 1 << 8 | 1 << 9)) // layer 8 is Vertex, 9 is Edge
				{
					isSelecting = true;
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
							}
							else
							{
								V.Remove (vertex);
							}
						}
						else
						{
							this.EmptySelected ();
							V.Add (vertex);
							vertex.SetSelected (true);
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
							}
							else
							{
								E.Remove (edge);
							}
						}
						else
						{
							this.EmptySelected ();
							E.Add (edge);
							edge.SetSelected (true);
						}
					}
				}
			// clicked on nothing
			else
				{
					if (!Input.GetKey (KeyCode.LeftShift))
					{
						this.EmptySelected ();
					}
				}
			}
		}

		if (!(isSelecting || isMoving))
		{
			// right click
			if (Input.GetMouseButtonDown (1))
			{
				Debug.Log ("Right click");
				isTurning = true;
			}
			if (isTurning)
			{
				// get mouse movement
				float mouseX = Input.GetAxis ("Mouse X");
				float mouseY = -Input.GetAxis ("Mouse Y");
				lookRot.y += mouseX * sensitivity * Time.deltaTime;
				lookRot.x += mouseY * sensitivity * Time.deltaTime;

				// clamp to prevent flipping
				lookRot.x = Mathf.Clamp(lookRot.x, -camClampAngle, camClampAngle);

				// rotate camera
				transform.rotation = Quaternion.Euler(lookRot);

				Debug.Log ("Turning");
			}
		}

		if (!(isSelecting || isTurning))
		{
			// middle click or left control
			if (Input.GetMouseButtonDown (2))
			{
				isMoving = true;
				Debug.Log ("Middle Click");
			}
			if (isMoving)
			{
				// get mouse movement
				float mouseX = Input.GetAxis ("Mouse X");
				float mouseY = Input.GetAxis ("Mouse Y");

				// move camera
				Vector3 dir = -(mouseX * transform.right + mouseY * transform.up) * moveSpeed * Time.deltaTime;
				con.Move (dir);
			}
			else
			{
				if (V.Count == 0)
				{
					float mouseScroll = Input.GetAxis ("Mouse ScrollWheel");
					Vector3 dir = mouseScroll * transform.forward * scrollSpeed * Time.deltaTime;
					con.Move (dir);
				}
			}
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


	public void AddEdge (Edge edge)
	{
		E.Add (edge);
	}
}

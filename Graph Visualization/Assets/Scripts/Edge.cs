using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Edge : MonoBehaviour {

	// Graph
	private Graph master; // parent graph

	// Vertices
	private Vertex startVertex; // start vertex
	private Vertex endVertex; // end vertex
	private bool hasStartVertex = false;
	private bool hasEndVertex = false;
	private Vector3 startPosition = Vector3.zero; // position of startVertex
	private Vector3 endPosition = Vector3.right; // " of endVertex

	// Type and weight
	private bool directed = false; // false --> simple, true --> directed
	private float weight = 1f;

	// params for selection and visual
	public bool isSelected = false;
	private LineRenderer renderer;
	public Material unselectedMaterial;
	public Material selectedMaterial;


	void Start ()
	{
		// set endpoints
		startPosition = transform.localPosition;
		endPosition = transform.localPosition + transform.forward * transform.lossyScale.z;
		renderer = GetComponent<LineRenderer> ();
	}


	void Update ()
	{
		UpdatePosition ();
	}


	public void SetMaster (Graph master)
	{
		this.master = master;
	}


	// set or change startVertex
	public void SetStartVertex (Vertex startVertex)
	{
		// if startVertex has been assigned
		if (hasStartVertex)
		{
			// if endVertex has been assigned
			if (hasEndVertex)
			{
				// disconnect current startVertex from edge
				this.startVertex.RemoveConnection (this);

				// change start vertex assignment
				this.startVertex = startVertex;

				// connect new startVertex to edge
				this.startVertex.AddConnection (this);
			}
			// there is no endVertex, so no connection
			else
			{
				this.startVertex = startVertex;
			}
		}
		// no startVertex has been assigned
		else
		{
			this.startVertex = startVertex;
			this.hasStartVertex = true;

			// if there was an endVertex, both are now set, connect
			if (hasEndVertex)
			{
				this.startVertex.AddConnection (this);

				if (!directed)
				{
					this.endVertex.AddConnection (this);
				}
			}
		}
	}


	public void SetEndVertex (Vertex endVertex)
	{
		if (hasEndVertex)
		{
			if (hasStartVertex)
			{
				if (directed)
				{
					this.endVertex = endVertex;
				}
				else
				{
					this.endVertex.RemoveConnection (this);
					this.endVertex = endVertex;
					this.endVertex.AddConnection (this);
				}
			}
			else
			{
				this.endVertex = endVertex;
			}
		}
		else
		{
			this.hasEndVertex = true;
			this.endVertex = endVertex;

			if (hasStartVertex)
			{
				startVertex.AddConnection (this);

				if (!directed)
				{
					this.endVertex.AddConnection (this);
				}
			}
		}
	}


	public void UpdatePosition ()
	{
		// update endpoint locations
		if (hasStartVertex)
		{
			startPosition = startVertex.transform.localPosition;
		}

		if (hasEndVertex)
		{
			endPosition = endVertex.transform.localPosition;
		}

		// move start point
		transform.localPosition = startPosition;

		// get displacement to end point
		Vector3 displacement = endPosition - startPosition;

		// set length
		transform.localScale = new Vector3(1, 1, displacement.magnitude);

		// set orientation
		if (displacement != Vector3.zero)
		{
			transform.localRotation = Quaternion.LookRotation (displacement);
		}
	}


	public void SetWeight (float weight)
	{
		this.weight = weight;
	}


	public float GetWeight ()
	{
		return this.weight;
	}


	public void SetDirected(bool directed)
	{
		// if directed is changing, adjust adjacencies accordingly
		if (hasStartVertex && hasEndVertex)
		{
			if (!this.directed && directed)
			{
				this.endVertex.RemoveConnection (this);
			}
			else if (this.directed && !directed)
			{
				this.endVertex.AddConnection (this);
			}
		}

		// set directed
		this.directed = directed;
	}


	public void SetSelected(bool isSelected)
	{
		if (this.isSelected == !isSelected)
		{
			this.isSelected = isSelected;
			if (isSelected)
			{
				renderer.material = selectedMaterial;
			}
			else
			{
				renderer.material = unselectedMaterial;
			}
		}
	}


	public void ToggleSelected ()
	{
		SetSelected (!isSelected);
	}


	public void PingSelect (Vertex vertex)
	{
		if (!isSelected)
		{
			if (hasStartVertex)
			{
				if (startVertex.isReceiving && startVertex != vertex)
				{
					master.user.AddEdge (this);
				}
			}

			if (hasEndVertex)
			{
				if (endVertex.isReceiving && endVertex != vertex)
				{
					master.user.AddEdge (this);
				}
			}
		}
	}


	public bool IsIsolated ()
	{
		return !(hasStartVertex || hasEndVertex);
	}


	// moves edge; does will not move edges which are connected, unless connected vertex is also selected
	public void Move (Vector3 dir)
	{
		startPosition += dir;
		endPosition += dir;
	}
}

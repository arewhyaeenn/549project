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


	public void SetStartVertex (Vertex startVertex)
	{
		if (hasStartVertex)
		{
			if (hasEndVertex)
			{
				this.startVertex.RemoveConnection (this);
				this.startVertex = startVertex;
				this.startVertex.AddConnection (this);
			}
			else
			{
				this.startVertex = startVertex;
			}
		}
		else
		{
			this.startVertex = startVertex;
			this.hasStartVertex = true;

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
}

Stream of Thought
===================

* To construct::

    stream = Stream(controller)
    
* The only relevant function here is FocusOn. It takes a focusable entity::

    self.FocusOn(focusable)
    
    
Focusable Mixin
==================

Entities that can be focused on should mix this in, and provide the following methods.

* If some work needs be done when focused upon, it can be done in the *FocusOn* method. This
  is for immediate book-keeping-like stuff. *GetAffordance* below can handle the creation
  of codelets for latter activity::
  
    self.FocusOn(controller)

* The fringe of the entity is a dictionary keyed by fringe elements and with floats
  indicating intensity as value::
  
    fringe = self.GetFringe(controller)
    
* Affordances are codelets that have not yet been added to the coderack::

    affordances = self.GetAffordance(controller)
    
* Similarity affordances are generated when the fringe of a new entity being focused on
  significantly overlaps that of an existing entity::
  
    codelets = older_focus.GetSimilarityAffordances(new_focus, older_fringe, new_fringe,
                                                    controller) 
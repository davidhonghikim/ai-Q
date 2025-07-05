// This is a stub/example for future drag-and-drop features using @dnd-kit/sortable.
// To use: import and render <SortableList /> in your dashboard page.
// For more, see https://docs.dndkit.com/presets/sortable
// If you add new sortable features, update this stub and document usage for future agents.

import * as React from 'react';
import { DndContext, DragEndEvent } from '@dnd-kit/core';
import { SortableContext, arrayMove, useSortable, verticalListSortingStrategy } from '@dnd-kit/sortable';

// Example items
const defaultItems: string[] = ['Item 1', 'Item 2', 'Item 3'];

export function SortableList() {
  const [items, setItems] = React.useState<string[]>(defaultItems);

  return (
    <DndContext onDragEnd={(event: DragEndEvent) => {
      const {active, over} = event;
      if (over && active.id !== over.id) {
        setItems((items) => arrayMove(items, items.indexOf(active.id as string), items.indexOf(over.id as string)));
      }
    }}>
      <SortableContext items={items} strategy={verticalListSortingStrategy}>
        {items.map((id: string) => <SortableItem key={id} id={id} />)}
      </SortableContext>
    </DndContext>
  );
}

function SortableItem({id}: {id: string}) {
  const {attributes, listeners, setNodeRef, transform, transition, isDragging} = useSortable({id});
  return (
    <div ref={setNodeRef} style={{
      transform: transform ? `translateY(${transform.y}px)` : undefined,
      transition,
      opacity: isDragging ? 0.5 : 1,
      border: '1px solid #ccc',
      padding: 8,
      marginBottom: 4,
      background: '#fff',
      borderRadius: 4,
      cursor: 'grab',
    }} {...attributes} {...listeners}>
      {id}
    </div>
  );
} 
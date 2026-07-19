# Webapp taxonomy & seed library

Seeds anchor on a component/interaction RULE (which supplies difficulty + deterministic
checkability). Industry × archetype are orthogonal theming axes any seed drops into.
Every seed row MUST have an `assertion_hint` (how it is checked in vitest/jsdom).

## industries
| id | description |
| saas | B2B software product marketing site |
| dental_clinic | local dental practice |
| restaurant | independent restaurant / cafe |
| fitness_studio | boutique gym / fitness studio |

## archetypes
| id | description |
| landing | hero + marketing sections (features/pricing/FAQ/footer) |
| lead_gen | contact/booking page centered on a form |

## seeds

### nav
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| mobile_menu_close_on_navigate | tapping a menu link closes the mobile menu | on phone the menu stays open covering the page after choosing a destination | open menu (click nav-toggle), click a link in mobile-menu, assert queryByTestId mobile-menu is null | t0 | scroll_spy_active_link |
| scroll_spy_active_link | the in-view section's nav link is marked active | the nav never highlights where you are on the page | mock IntersectionObserver in setup; drive a section into view; assert its link has the active class or aria-current true | t2-t3 | mobile_menu_close_on_navigate |

### accordion
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| accordion_single_open | opening one FAQ item closes the others | multiple FAQ answers stay expanded at once | open item A then item B, assert exactly one faq-answer in the document | t0 | a11y_labels_alt |

### grid
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| responsive_grid_collapse | the card grid is one column on mobile, multi on desktop | cards stay in a cramped multi-column row on phones | assert the grid element className contains grid-cols-1 and a md:grid-cols- class | t0 | filter_list |

### a11y
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| a11y_labels_alt | images have alt text, icon-buttons have aria-label, inputs have labels | screen readers cannot announce images or controls | assert every img has non-empty alt, icon buttons expose an accessible name, getByLabelText finds each input | t0-t1 | form_validation_gating |

### pricing
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| pricing_most_popular | exactly the intended tier carries the most-popular highlight | the highlight is missing or on the wrong plan | assert exactly one popular-badge and it is within the intended tier matched by name or order | t1 | tabs_active_panel |

### form
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| form_validation_gating | submitting invalid input is blocked and shows errors | the contact form submits even when required fields are empty or bad | submit empty then assert error messages shown and no success state, fill valid then assert success state | t1 | controlled_input_state |
| controlled_input_state | inputs are controlled and reflect typed text | typing in a field does nothing or the value never updates | user-event type into the input, assert input value equals the typed text | t2 | form_validation_gating |

### tabs
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| tabs_active_panel | selecting a tab shows only its panel | wrong panel shows or multiple panels show at once | click tab 2, assert exactly one tabpanel visible and it is panel 2 with aria-selected true | t1 | pricing_most_popular |

### modal
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| modal_close_overlay_esc | the modal closes on overlay click and on Escape | the popup will not dismiss without the X button | open modal, click overlay assert gone, reopen, press Escape assert gone | t1-t2 | controlled_input_state |

### carousel
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| carousel_wrap_bounds | next and prev wrap within bounds, never off the ends | the testimonial slider goes blank past the last slide | click next past the end, assert the active slide index wraps or stays within range | t2 | filter_list |

### filter
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| filter_list | category buttons filter the list and All restores it | filtering does nothing or All hides everything | click a category assert only matching items render, click All assert full set renders | t2 | responsive_grid_collapse |

## difficulty_principles

- Reason-it-out, not recalled-reflex: a t2+ defect must be a repo-specific rule the
  student reads and reasons about, not a canonical fix it recalls. t0/t1 seeds may be
  single-component reflexes (a missing onClick, a missing responsive class).
- Difficulty = reasoning depth, not page size. More sections or copy is not harder.
- Coupling is a multiplier on already-unfamiliar defects, via couples_with: cross-component
  state (scroll_spy + mobile_menu_close), form state (form_validation + controlled_input),
  layout+behavior (filter_list + responsive_grid_collapse). Coupling easy reflexes does not
  create difficulty.
- Tier intent: t0 = one single-component reflex; t1 = one non-obvious single-component rule;
  t2+ = coupled / cross-component reasoning or state/observer subtleties. Bands are measured
  in SP4.
- Determinism: every seed's assertion_hint must be a deterministic vitest/jsdom assertion.
  Observer/timer seeds (scroll_spy_active_link) must mock the boundary (IntersectionObserver)
  in setup.ts.

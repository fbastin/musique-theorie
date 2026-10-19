\version "2.24.3"
%% Fichier produit par outils/generer_interpretation.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
psubito = #(make-dynamic-script (markup #:dynamic "p" #:hspace 0.6 #:normal-text #:italic "subito"))
\score {
  \new Staff  {
      \clef treble \time 4/4 \override TextScript.staff-padding = #5
      c''4\p\<_\markup \small \italic "crescendo" d'' e'' f'' | g''2\f\>_\markup \small \italic "decrescendo" e''2 | c''1\p |
      c''4\cresc d'' e'' f'' | \break g''1\f |
      c''4\p d'' e''\sfz_\markup \small \italic "sforzando" f'' | g''2\fp_\markup \small \italic "forte-piano" g''2 | c''2\f g''2\psubito
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}

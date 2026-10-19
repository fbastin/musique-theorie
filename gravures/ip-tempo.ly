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
\score {
  \new Staff  {
      \clef treble \time 4/4 \tempo "Allegro" 4 = 132
      \override TextSpanner.bound-details.left.text = \markup \italic "rit."
      \override TextSpanner.staff-padding = #2.5
      g'4 c'' e'' g'' | e''4 c'' g'2 |
      c''4\startTextSpan d'' e'' f'' | g''2 g''2\stopTextSpan |
      c''4^\markup \italic "a tempo" e'' g'' c''' | c'''1
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
